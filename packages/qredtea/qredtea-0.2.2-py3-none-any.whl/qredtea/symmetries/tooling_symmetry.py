# This code is part of qredtea.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Tooling for Abelian symmetries. For now, it is in qredtea as tooling for
symmetries (open to move it somewhere else).
"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches

import numpy as np
import qtealeaves as qtl

from qredtea.tooling import QRedTeaAbelianSymError

from .abeliantensor import AbelianSymmetryInjector, QteaAbelianTensor

__all__ = [
    "LocalAbelianSymmetryInjector",
]


class LocalAbelianSymmetryInjector(AbelianSymmetryInjector):
    """
    Symmetry injector for usage with local symmetries or other setups,
    where more than a global projection is needed.

    Arguments
    ---------

    sectors : dict | None
        If dictionary, contains key-value pairs with keys being tensor
        position in the network and values being :class:`IrrepListing`
        used as projector.
    """

    def __init__(self, sectors=None):
        self.sectors = sectors

    def inject_parse_sectors(self, params, sym):
        sym = self.sectors["global"].sym

        return sym, self.sectors


def represent_local_symmetries_by_global(local_syms, num_sites, curve):
    """
    Find a representation of local symmetries as global symmetries in a TTN.

    Arguments
    ---------

    local_syms : list[tuple[...]]
        The local symmetries are passed as list of tuples, where each tuple
        contains the description of a local symmetry with the following entries.
        1) list of sites, sites are specified as a tuple of ints. 2) list of
        operators as strings corresponding to the generator of the local symmetry
        on each site. 3) str with the symmetry type as different local symmetries
        cannot be represented by one global symmetry. 4) target irreps.

    num_sites : int
        Number of sites in the system to generate a dummy-tree, where the dummy
        tree generates the paths between tensors.

    curve : :class:`HilbertCurveMap`
        Mapping for a system in n-D into 1-D.

    Returns
    -------

    global_syms : list[dict]
        The return value is a list of dictionaries where each dictionary
        encodes a global symmetry. The dictionary contains the following keys
        ``elem`` : listed list with position in 1d system and operator string
        for generator, i.e., ``[[[1, 2], ["A", "B"]], [[7, 8], ["C", "B"]], ...]``;
        ``type`` : symmetry type' ``blocked_pos`` : set with tensor positions
        blocked by local symmetries. position keys are added on top with their
        irrep.
    """
    global_syms = []

    conv_params = qtl.convergence_parameters.TNConvergenceParameters()
    psi = qtl.emulator.TTN(num_sites, conv_params)

    required_paths = []
    path_lengths = []
    proj_positions = []

    for sites_nd, ops, stype, irrep in local_syms:
        sites_1d = [curve[site] for site in sites_nd]

        required_pos = []
        for ii, site_a in enumerate(sites_1d):
            pos_a = (psi.num_layers - 1, site_a // 2)
            required_pos.append(pos_a)
            for site_b in sites_1d[:ii]:
                pos_b = (psi.num_layers - 1, site_b // 2)
                path = psi.get_path(pos_b, start=pos_a)
                for elem in path:
                    required_pos.append(tuple(elem[3:5]))

        required_pos = set(required_pos)
        pos_proj = None
        for elem in required_pos:
            if pos_proj is None:
                pos_proj = elem
            if elem == (0, 0):
                pos_proj = elem
            elif elem[0] < pos_proj[0]:
                pos_proj = elem

        required_paths.append(required_pos)
        path_lengths.append(len(required_pos))
        proj_positions.append(pos_proj)

    path_lengths = np.array(path_lengths, dtype=int)
    inds = np.argsort(path_lengths)

    for ii in inds[::-1]:
        sites_nd, ops, stype, irrep = local_syms[ii]
        required_pos = required_paths[ii]
        pos_proj = proj_positions[ii]
        sites_1d = [curve[site] for site in sites_nd]

        # Check existing symmetries
        need_new_sym = True
        for sym_dict in global_syms:
            has_overlap = len(sym_dict["blocked_pos"].intersection(required_pos)) > 0
            if has_overlap:
                continue

            if sym_dict["type"] != stype:
                continue

            # Add to this symmetry
            sym_dict["blocked_pos"] = sym_dict["blocked_pos"].union(required_pos)
            sym_dict["elem"].append([sites_1d, ops])
            sym_dict[pos_proj] = irrep
            need_new_sym = False
            break

        if need_new_sym:
            # Create new symmetry
            new_sym = {
                "blocked_pos": required_pos,
                "elem": [[sites_1d, ops]],
                "type": stype,
                pos_proj: irrep,
            }
            global_syms.append(new_sym)

    return global_syms


def transformation_basis(op_dict, symmetries, generators, params):
    """
    Build a function which can undo the permutation initially executed
    for the irreps. Necessary for a workflow where we have a symmetric
    tensor network, transform it into a dense network, and then execute
    sampling (or rely on the original order of the states in the Hilbert
    space).

    Arguments
    ---------

    op_dict : :class:`TNOperators`
        Contains the operator sets used for the Quantum TEA simulation.

    symmetries : list[:class:`_AbstractAbelianSymGroup`]
        Contains the symmetries used in the simulation.

    generators : list
        List of the generators, e.g., their string which are found in
        the operator dictionary.

    params : dict
        Parameterization of the simulation as dictionary.

    Returns
    -------

    mapping: callable
        Function can be called with site (1d) and a value, i.e.,
        index in the Hilbert space, which is translated into the
        original label.
    """
    if len(symmetries) != len(generators):
        print("Error information", symmetries, generators)
        raise QRedTeaAbelianSymError("Generator and symmetry lengths do not match.")

    # pylint: disable-next=dangerous-default-value,unused-argument
    def transform(key, op, params=params):
        if isinstance(op, str):
            op = params[op]
        op = qtl.tensors.QteaTensor.from_elem_array(op.copy())
        op.convert(None, "cpu")

        if op.ndim == 4:
            op.remove_dummy_link(3)
            op.remove_dummy_link(0)

        return op

    tmp_op = op_dict.transform(transform)

    inds_dict = {}
    for name in tmp_op.set_names:
        # pylint: disable-next=protected-access
        tmp_op = tmp_op._ops_dicts[name]

        # pylint: disable-next=protected-access
        _, inds, _ = QteaAbelianTensor._parse_generators(tmp_op, symmetries, generators)

        inds_dict[name] = inds

    # inds_dict is not modified in the following function and
    # therefore we allow passing a dict as optional argument
    # pylint: disable-next=dangerous-default-value
    def mapping(site, value, inds_dict=inds_dict):
        irrep_inds = inds_dict[str(site)]
        return irrep_inds[value]

    return mapping
