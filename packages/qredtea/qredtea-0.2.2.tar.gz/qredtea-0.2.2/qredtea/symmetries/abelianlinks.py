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
Abelian links and link weights for qtealeaves module.
"""

# pylint: disable=too-many-locals

import warnings
from copy import deepcopy

import numpy as np
from qtealeaves.tensors import QteaTensor

from qredtea.tooling import QRedTeaAbelianSymError, QRedTeaError, QRedTeaLinkError

from .couplingsectors import CouplingSectors
from .ibarrays import bmaskf, bmaskt, iany, iarray, ichoice, imax, isum, izeros
from .irreplistings import IrrepListing

__all__ = ["AbelianSymLink", "AbelianSymLinkWeight"]

RUN_SANITY_CHECKS = True


class AbelianSymLink:
    """

    **Arguments**

    sym : instance of `AbelianSymCombinedGroup`

    irrep_listing : instance of `IrrepListing`

    """

    def __init__(self, sym, irrep_listing):
        if sym != irrep_listing.sym:
            raise QRedTeaAbelianSymError(
                "Symmetry of irrep must match the one for link."
            )

        self._irrep_listing = irrep_listing

        # Irrep listing is write-protected so far, so it cannot be changed
        # Calculate the shape once
        self._shape = isum(self.irrep_listing.degeneracies)

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    def irrep_listing(self):
        """Irrep listing property."""
        return self._irrep_listing

    @irrep_listing.setter
    def irrep_listing(self, value):
        """Setter for irrep listing property updating as well the shape."""
        self._irrep_listing = value
        self._shape = isum(self.irrep_listing.degeneracies)

    @property
    def shape(self):
        """Dimension of the link summing up the degneracy dimensions."""
        return self._shape

    @property
    def sym(self):
        """Symmetry property which must be equal to the irreps' symmetry."""
        return self.irrep_listing.sym

    # --------------------------------------------------------------------------
    #                          Overwritten operators
    # --------------------------------------------------------------------------

    def __eq__(self, other):
        return self.irrep_listing == other.irrep_listing
        # if self.sym != other.sym:
        #    return False

        # if self.irrep_listing != other.irrep_listing:
        #    return False

        # return True

    def __int__(self):
        """Returning shape via int-method."""
        return int(self.shape)

    def __lt__(self, other):
        """Comparing link based on shape."""
        return int(self) < int(other)

    def __ne__(self, other):
        return not self == other

    # --------------------------------------------------------------------------
    #                       classmethod, classmethod like
    # --------------------------------------------------------------------------

    @classmethod
    def create_dummy(cls, sym):
        """
        Create a dummy link with the identical irrep.

        **Argument**

        sym : instance of `AbelianSymCombinedGroup`
        """
        irrep = sym.identical_irrep
        irrep = irrep.reshape((1, irrep.shape[0]))
        degeneracies = iarray([1])

        return cls(sym, IrrepListing.from_irreps(sym, irrep, degeneracies))

    @classmethod
    def from_link_list(cls, links, are_links_outgoing=None):
        """
        Couple the irreps from a list of links to generate a new link.

        **Arguments**

        links : list of `AbelianSymLink`

        are_links_outgoing : list of boolean, (mandatory here)
            Describes the link direction.
            Default to `None`, but required here.
        """
        if are_links_outgoing is None:
            raise QRedTeaLinkError("Link directions are missing for symmetric tensors.")

        # Get new link (all combinations)
        link = links[0].product_couple(
            links[1],
            invert_self=are_links_outgoing[0],
            invert_other=are_links_outgoing[1],
        )

        for ii in range(2, len(links)):
            link = link.product_couple(links[ii], invert_other=are_links_outgoing[ii])

        return link

    def invert(self):
        """Invert the irreps and return a new link with the inverted irreps (order changes)."""
        if len(self.irrep_listing) == 0:
            return self

        irreps = self.irrep_listing.irreps
        irreps = self.sym.invert_irrep(irreps)
        irrep_listing = IrrepListing.from_irreps(
            self.sym, irreps, self.irrep_listing.degeneracies
        )

        return AbelianSymLink(self.sym, irrep_listing)

    def remove_trivial(self):
        """Generate a new link which has no trivial irreps with degeneracy zero."""
        irrep_listing = IrrepListing.from_irreps(
            self.sym,
            self.irrep_listing.irreps,
            self.irrep_listing.degeneracies,
            are_sorted=True,
            remove_trivial=True,
            are_unique=True,
        )

        return AbelianSymLink(self.sym, irrep_listing)

    # --------------------------------------------------------------------------
    #                            Checks and asserts
    # --------------------------------------------------------------------------

    def sanity_check(self, require_trivial_removed=False):
        """Run small checks to ensure nothing obvious is broken."""
        if self.sym != self.irrep_listing.sym:
            raise QRedTeaAbelianSymError("Symmetry mismatch")

        if require_trivial_removed:
            remove_trivial = self.remove_trivial()
            if remove_trivial != self:
                raise QRedTeaAbelianSymError(
                    "Link contains trivial irreps with 0-degeneracy."
                )

        self.irrep_listing.sanity_check()

    # --------------------------------------------------------------------------
    #                            Remaining methods
    # --------------------------------------------------------------------------

    def helper_split(self, other):
        """
        Helps with splitting a tensor via decompositions. Will adapt the degneracy
        dimension to the minimum of both as valid in QR and SVD. Inplace update.

        **Arguments**

        other : instance of `AbelianSymLink`
        """
        degs_a = self.irrep_listing.degeneracies.copy()
        degs_b = other.irrep_listing.degeneracies.copy()

        mask_b = bmaskt(len(degs_b))

        for ii in range(self.irrep_listing.irreps.shape[0]):
            irrep_a = self.irrep_listing.irreps[ii, :]

            jj = other.irrep_listing.index(irrep_a)

            if jj is None:
                # irrep is not other
                degs_a[ii] = 0
                continue

            # Mark entry jj as visited
            mask_b[jj] = False

            deg_a = self.irrep_listing.degeneracies[ii]
            deg_b = other.irrep_listing.degeneracies[jj]

            deg = min(deg_a, deg_b)

            degs_a[ii] = deg
            degs_b[jj] = deg

        degs_b[mask_b] = 0

        irrep_list_a = IrrepListing.from_irreps(
            self.sym,
            self.irrep_listing.irreps,
            degs_a,
            are_sorted=True,
            # remove_trivial=True,
            are_unique=True,
        )

        irrep_list_b = IrrepListing.from_irreps(
            other.sym,
            other.irrep_listing.irreps,
            degs_b,
            are_sorted=True,
            # remove_trivial=True,
            are_unique=True,
        )

        if RUN_SANITY_CHECKS:
            if iany(self.irrep_listing.irreps != irrep_list_a.irreps):
                raise QRedTeaAbelianSymError("Order in irreps changed (self).")

            if iany(other.irrep_listing.irreps != irrep_list_b.irreps):
                raise QRedTeaAbelianSymError("Order in irreps changed (other).")

        return AbelianSymLink(self.sym, irrep_list_a), AbelianSymLink(
            other.sym, irrep_list_b
        )

    def _random_reduce(self, target_dim):
        """
        Randonmly reduce the dimension by cutting down some of the
        degeneracy dimensions.

        **Arguments**

        target_dim : int
            Target dimension after reducing the bond dimension. Muist be
            smaller than the current dimension.

        **Returns**

        link : instance of `AbelianSymLink`
            New link with new degeneracies and potentially eliminated
            irreps.

        deg_mask_dict : dict
            Keys are the coupling in the old link and the value
            contains a mask to reduce the dimension from the previous
            degeneracy dimension to the new degeneracy dimension.
        """
        dim = self.shape

        if target_dim >= dim:
            raise QRedTeaError("Target dimensions not smaller than  current dimension.")

        inds = ichoice(dim, size=target_dim, replace=False)
        mask = bmaskf(dim)
        mask[inds] = True

        k2 = 0

        deg_mask_dict = {}
        nn = self.irrep_listing.irreps.shape[0]
        mask_irreps = bmaskt(nn)
        new_degeneracies = izeros(nn)
        idx = -1
        for ii in range(nn):
            k1 = k2
            k2 += self.irrep_listing.degeneracies[ii]

            mm = isum(mask[k1:k2])
            if mm == 0:
                mask_irreps[ii] = False
            else:
                idx += 1
                deg_mask_dict[idx] = mask[k1:k2]
                new_degeneracies[ii] = mm

        irreps = self.irrep_listing.irreps[mask_irreps, :]
        new_degeneracies = new_degeneracies[mask_irreps]
        irrep_listing = IrrepListing.from_irreps(
            self.sym, irreps, new_degeneracies, are_sorted=True, are_unique=True
        )

        link = AbelianSymLink(self.sym, irrep_listing)

        return link, deg_mask_dict

    def random_expand(self, full_link, target_dim):
        """
        Returns link with degeneracies to be added for random expansion to current
        link.
        """
        dim = target_dim - self.shape
        if dim < 1:
            raise QRedTeaError(
                f"Cannot expand because target dim {target_dim} smaller equal current {self.shape}."
            )

        deg = full_link.irrep_listing.degeneracies.copy()

        idx = 0
        for ii in range(len(self.irrep_listing)):
            irrep = self.irrep_listing.irreps[ii, :]
            idx = full_link.irrep_listing.index(
                irrep, start_idx=idx, require_match=True
            )

            # if idx is None:
            #    raise QRedTeaAeblianSymError("irrep must be present in full link.")

            deg[idx] -= self.irrep_listing.degeneracies[ii]

            if deg[idx] < 0:
                warnings.warn(
                    # raise QRedTeaError(
                    "deg dimension in full link must be bigger than in link."
                )

                deg[idx] = 0

        dim_avail = isum(deg)
        dim = min(dim, dim_avail)
        inds = ichoice(dim_avail, size=dim, replace=False)
        mask = bmaskf(dim_avail)
        mask[inds] = True

        k2 = 0
        for ii, deg_ii in enumerate(deg):
            k1 = k2

            # Retrieve old dimension
            k2 += deg_ii

            # Update dimension
            deg[ii] = isum(mask[k1:k2])

        irrep_listing = IrrepListing.from_irreps(
            self.sym,
            full_link.irrep_listing.irreps,
            deg,
            are_sorted=True,
            are_unique=True,
            remove_trivial=True,
        )

        link = AbelianSymLink(self.sym, irrep_listing)

        return link

    def product_couple(self, other, invert_self=False, invert_other=False):
        """
        Build all possible combinations of irreps between the link
        and another link.

        **Arguments**

        other : instance of `AbelianSymLink`
            Second link where we iterate over all irreps in link.

        invert_self : bool, optional
            Flag if irreps on `self` should be inverted.
            Default to `False`

        invert_other : bool, optional
            flag if irreps on `other` should be inverted.
            Default to `False`
        """
        irrep_listing = self.irrep_listing.product_couple(
            other.irrep_listing,
            invert_self=invert_self,
            invert_other=invert_other,
        )

        return AbelianSymLink(self.sym, irrep_listing)

    def restrict_irreps(self, irrep_listing):
        """
        Restrict the irreps in the link to the irreps passed. Degeneracies are
        also restricted. Update is inplace.

        **Arguments**

        irrep_listing : instance of `IrrepListing` or None
            All irreps from here will remain in the link. Irreps
            which are here but not in the link, will not be added.
            Degeneracies will be calculated based on the minimum
            of the two.
        """
        # self.sanity_check()

        if irrep_listing is None:
            # Nothing to-do
            return self

        degeneracies = deepcopy(self.irrep_listing.degeneracies)

        for ii in range(len(self.irrep_listing)):
            irrep = self.irrep_listing.irreps[ii, :]

            idx = irrep_listing.index(irrep)

            if idx is None:
                degeneracies[ii] = 0
            else:
                degeneracies[ii] = min(
                    degeneracies[ii], irrep_listing.degeneracies[idx]
                )

        if imax(degeneracies) == 0:
            warnings.warn(
                "Restricting failed; global irreps are"
                + f" [len={len(self.irrep_listing.irreps)}]: "
                + f"{[ list(ir) for ir in self.irrep_listing.irreps ]}"
            )
            raise QRedTeaAbelianSymError("Restricting irreps leads to empty irreps.")

        self.irrep_listing = IrrepListing.from_irreps(
            self.sym,
            self.irrep_listing.irreps,
            degeneracies,
            are_sorted=True,
            remove_trivial=True,
            are_unique=True,
        )

        return self

    def select_irreps(self, inds, do_return_deg=False):
        """
        Select and return the irreps at given indices.

        **Arguments**

        inds : int
            Return irreps of selected indices

        do_return_deg : bool, optional
            If true, in addition to irreps the degeneracies
            are returned as second return value.
            Default to false.
        """
        if do_return_deg:
            return (
                self.irrep_listing.irreps[inds, :],
                self.irrep_listing.degeneracies[inds],
            )

        return self.irrep_listing.irreps[inds, :]

    def stack_link(self, other):
        """Stacking link executes an union of the underlying irreps returning a new link."""
        irrep_union = self.irrep_listing.union(other.irrep_listing)

        return AbelianSymLink(self.sym, irrep_union)

    def generate_cs(self, irreps):
        """
        Generate the coupling sectors for the link through the
        passed irreps which are active.

        **Arguments**

        irreps : np.ndarray, rank-2, int-type
            active irreps, unsorted, non-unique allowed
            Unsorted because of original order in degeneracy tensors
            list.

        **Returns**

        cs : np.ndarray, rank-1
            Coupling sector indices of irreps in link, ordered ascendingly.

        degeneracies : np.ndarray, rank-1
            Degeneracies, same order as cs.

        inds : vector
            For ordering incoming irreps the same as information
            in cs. Result of argsort.
        """
        inds = IrrepListing.argsort_irreps(irreps)
        cs = izeros(inds.shape[0])
        degeneracies = izeros(inds.shape[0])

        # index for link irreps
        ii = 0

        # index for CS irreps
        jj = 0

        nn = self.irrep_listing.irreps.shape[0]
        nn += irreps.shape[0]
        for _ in range(nn):
            irrep_ii = self.irrep_listing.irreps[ii, :]
            irrep_jj = irreps[inds[jj], :]

            if IrrepListing.is_equal_irrep(irrep_ii, irrep_jj):
                # Match, save information and increment only jj
                # as it can be non-unique
                degeneracies[jj] = self.irrep_listing.degeneracies[ii]
                cs[jj] = ii

                jj += 1

            elif IrrepListing.is_smaller_irrep(irrep_ii, irrep_jj):
                ii += 1
            elif IrrepListing.is_greater_irrep(irrep_ii, irrep_jj):
                jj += 1
            else:
                raise QRedTeaError("What else can there be???")

            if jj == inds.shape[0]:
                break

            if ii >= len(self.irrep_listing):
                raise QRedTeaAbelianSymError("Something in CS without being in link?")

        return cs, degeneracies, inds

    @staticmethod
    def generate_fuse_rule(cs_fused, degeneracies, inds, cs_links):
        """
        Fuse rule is a helper to fuse and unfuse two links.

        **Arguments**

        cs_fused : np.ndarray, (arbitrary rows, one column)
            Fused coupling sector. Sorted.

        degeneracies : np.ndarray / list of ints
            Contains the degeneracies of each of the
            fused CS in `cs_fused[inds]`.

        inds : np.ndarray, rank-1
            Contains the output from argsort to sort the
            entries in `degeneracies` or `cs_links`

        cs_links : np.ndarray of rank-2
            Contains the coupling sectors before fusing.
            Unsorted.

        **Details**

        The fuse rule is a dictionary containing

        1) A dictionary accessible with the key `deg`. The dictionary
           contains the degeneracy based on the key of the new coupling
           sector.

        2) The other keys in the main dictionary are the tuples of
           the (old) coupling sectors. Each entry contains the new
           coupling sector, and the lower and upper index of the subtensors
           within the fused tensor, and the dimensions of the original
           subtensor.

        3) Higher-level functions can add an entry "link" with a
           link representing the degeneracy dimension after a qr-like
           decomposition, i.e., the minimum of the matrix dimensions.
        """
        # Could directly pass cdegs from `_fuse_prepare`
        cum_degeneracies = deepcopy(degeneracies[0])
        for elem in degeneracies[1:]:
            cum_degeneracies *= elem

        # To store original shape
        deg_links = iarray(degeneracies).transpose()

        fuse_rule_forward_a = {"deg": {}}
        last_cs = None
        last_bound = 0
        for ii in range(cs_fused.shape[0]):
            jj = inds[ii]
            key = tuple(cs_links[jj, :])

            if (cs_fused[ii] != last_cs) and (key in fuse_rule_forward_a):
                raise QRedTeaAbelianSymError(
                    "Cannot overwrite cs entry for unsorted fused cs."
                )

            # This is the right one, we report back via the key `deg_list`
            # so that the tensor can be created with the correct degeneracy
            if (cs_fused[ii] == last_cs) and (key in fuse_rule_forward_a):
                # Duplicates can occur which can happen as follows with Z2
                # 0 0 0 vs 0 0 0
                # 0 0 0 vs 1 0 1
                #
                # The matrix should look like
                #
                #          (0 0 0)  (1, 0, 1)
                #         ___________________
                # (0 0 0) |__________________|
                #
                #
                # Should be the same entry with the same degeneracy in my
                # opinion ... we continue
                continue
            if cs_fused[ii] == last_cs:
                k1 = last_bound
                k2 = k1 + cum_degeneracies[jj]
                last_bound = k2
            else:
                k1 = 0
                k2 = cum_degeneracies[jj]
                last_bound = k2
                last_cs = cs_fused[ii]

            fuse_rule_forward_a[key] = (
                last_cs,
                k1,
                k2,
                deg_links[jj, :],
            )

            # Update upper dimension of coupling sector (overwrite on purpose)
            fuse_rule_forward_a["deg"][last_cs] = k2

        tracker = {}
        irreps = izeros((len(fuse_rule_forward_a), len(key)))
        degs = []
        kk = -1
        for key, value in fuse_rule_forward_a.items():
            if key == "deg":
                continue

            if value[0] in tracker:
                continue

            kk += 1
            irreps[kk, :] = key
            degs.append(fuse_rule_forward_a["deg"][value[0]])
            tracker[value[0]] = None

        fuse_rule_forward_a["deg_list"] = iarray(degs)

        return fuse_rule_forward_a

    def intersection(self, other):
        """Return new link with interaction of two links, i.e., common irreps."""
        irrep_listing = self.irrep_listing.intersection(other.irrep_listing)
        return AbelianSymLink(self.sym, irrep_listing)

    def print_full(self, indent=0, label=""):
        """Debugging print with full information to stdout."""
        prefix = " " * indent
        print(prefix + "-" * 10 + " AbelianLink %s" % (label) + "-" * 10)
        print(prefix + "shape", self._shape)
        self.irrep_listing.print_full(indent=indent + 4)
        print(prefix + "^" * 34)


class AbelianSymLinkWeight:
    """
    Diagonal matrix for symmetric tensors, i.e., a link weight.

    **Arguments**

    link : instance of :class:`AbelianSymLink`

    sectors : integer array, rank-2

    link_weights : list of arrays with weights, same order as cs.

    base_tensor_cls : type
        Contains the base tensor class to perform default operations.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, link, sectors, link_weights, base_tensor_cls, allow_empty=False):
        self.link = link
        self.cs = CouplingSectors(sectors)
        self.link_weights = link_weights
        self.base_tensor_cls = base_tensor_cls

        if len(self) != len(link_weights):
            raise QRedTeaAbelianSymError(
                "Length of link weights does not match CS-length."
            )

        if len(self) == 0 and (not allow_empty):
            raise QRedTeaAbelianSymError("Preventing creation of empty link weights.")

    def __len__(self):
        return self.cs.num_coupling_sectors

    def __itruediv__(self, scalar):
        """In-place division of link-weights with scalar (update)."""
        link_weights_div = []
        for elem in self.link_weights:
            link_weights_div.append(elem / scalar)
        self.link_weights = link_weights_div

    def __pow__(self, power):
        link_weights_pow = []
        for elem in self.link_weights:
            link_weights_pow.append(elem**power)

        return AbelianSymLinkWeight(
            self.link,
            self.cs.denormalized_sectors,
            link_weights_pow,
            self.base_tensor_cls,
        )

    def __getitem__(self, key):
        idx_list = self.cs[key]
        if len(idx_list) > 1:
            raise QRedTeaAbelianSymError("Hashing all links should not lead to list.")
        return self.link_weights[idx_list[0]]

    def generate_hashes(self):
        """Hashes are always generated for the only diagonal link."""
        self.cs.generate_hashes([0])

    def sum(self):
        """Sum over all the entries of link weights returning scalar."""
        if len(self) == 0:
            return 0.0

        if hasattr(self.link_weights[0], "sum"):
            value = self.link_weights[0].sum()
        else:
            # Bold guess we have tensorflow
            value = float(self.link_weights[0].cpu().numpy().sum())

        for elem in self.link_weights[1:]:
            if hasattr(elem, "sum"):
                value += elem.sum()
            else:
                # Bold guess we have tensorflow
                value += elem.cpu().numpy().sum()

        return value

    def _empty_tensor(self):
        """Generate an example tensor based on the backend."""
        if self.base_tensor_cls == QteaTensor:
            if len(self) == 0:
                device = "cpu"
                tensor = self.base_tensor_cls([0])
                dtype = tensor.dtype_real()
            elif isinstance(self.link_weights[0], np.ndarray):
                device = "cpu"
                dtype = self.link_weights[0].dtype
            else:
                device = "gpu"
                dtype = self.link_weights[0].dtype
            tensor = self.base_tensor_cls([0], dtype=dtype, device=device)
        else:
            tensor = self.base_tensor_cls([0])
            if len(self) == 0:
                dtype = tensor.dtype_real()
            else:
                dtype = self.link_weights[0].dtype
            tensor = self.base_tensor_cls([0], dtype=dtype)

        return tensor

    def flatten(self):
        """
        Flatten the weights, i.e. concatenate the link_weight arrays
        across all the sectors.

        Returns
        -------

        vec : array (np.ndarray | to.Tensor | ...)
            Array of the same type as the underlying
            :class:`_AbstractQteaBaseTensor.elem`.
            Sorted in decaying order.
        """
        empty_tensor = self._empty_tensor()
        if len(self) == 0:
            # Example tensor is also empty tensor
            return empty_tensor.elem

        argsort, concatenate, flip = empty_tensor.get_attr(
            "argsort", "concatenate", "flip"
        )

        value = self.link_weights[0]
        for elem in self.link_weights[1:]:
            value = concatenate(value, elem)

        inds = argsort(value)
        value = value[inds]

        if empty_tensor.linear_algebra_library == "torch":
            value = flip(value, dims=(0,))
        else:
            value = value[::-1]

        return value

    def tolist(self):
        """
        Flatten the weights, i.e. concatenate the link_weight arrays
        across all the sectors. Values will be sorted in decaying order.

        Returns
        -------

        vec : list[float]
            Values sorted in decaying order.
        """
        if len(self) == 0:
            return []

        vec_flatten = self.flatten()
        empty_tensor = self._empty_tensor()
        vec_cpu = empty_tensor.get_of(vec_flatten)

        return [float(elem) for elem in vec_cpu]

    def sanity_check(self):
        """Sanity check for link weights."""
        if not RUN_SANITY_CHECKS:
            return

        assert self.cs.denormalized_sectors.shape[1] == 1
        assert self.cs.denormalized_sectors.shape[0] == len(self.link_weights)

        for jj, cs in enumerate(self.cs.denormalized_sectors[:, 0]):
            deg_link = self.link.irrep_listing.degeneracies[cs]
            deg_vec = len(self.link_weights[jj])

            if deg_link != deg_vec:
                msg = f"Degeneracy mismatch: {deg_link} (link) vs {deg_vec} (vector)"
                msg += f" at irreps {self.link.irrep_listing.irreps[cs, :]}."
                raise QRedTeaAbelianSymError(msg)
