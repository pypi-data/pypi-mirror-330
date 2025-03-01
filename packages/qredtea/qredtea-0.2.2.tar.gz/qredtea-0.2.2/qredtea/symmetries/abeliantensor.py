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
Abelian symmetry tensor class
"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-arguments
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-lines

# pylint: disable=protected-access


import itertools
import pickle
import warnings
from contextlib import nullcontext
from copy import deepcopy

import numpy as np
from qtealeaves.solvers import EigenSolverH

# pylint: disable-next=no-name-in-module
from qtealeaves.tensors import QteaTensor, TensorBackend, _AbstractQteaTensor
from qtealeaves.tooling.permutations import _transpose_idx
from scipy.sparse.linalg import ArpackError

from qredtea.tooling import (
    QRedTeaAbelianSymError,
    QRedTeaEmptyTensorError,
    QRedTeaError,
    QRedTeaLinkError,
    QRedTeaRankError,
)

from .abelianlinks import AbelianSymLink, AbelianSymLinkWeight
from .couplingsectors import CouplingSectors
from .ibarrays import (
    bmaskf,
    bmaskt,
    iall,
    iany,
    iarray,
    ilogical_not,
    imax,
    imaximum,
    imin,
    indarray,
    iones,
    iproduct,
    isum,
    izeros,
)
from .irreplistings import IrrepListing
from .symmetrygroups import AbelianSymCombinedGroup, AbelianSymU1, AbelianSymZN

__all__ = ["QteaAbelianTensor", "AbelianSymmetryInjector", "default_abelian_backend"]

RUN_SANITY_CHECKS = True
ENABLE_MULTIPLE_SYM = True


class QteaAbelianTensor(_AbstractQteaTensor):
    """
    Abelian tensor for Quantum Tea simulations.

    **Arguments**

    links : list of :class:`AbelianSymLink` instances
        Specifies the links in the tensor.

    ctrl : str, optional
        Initialization of tensor, either "N" (empty tensor
        without coupling sectors), "R", "random" (random),
        Default to "N"
        Valid data type for the underlying tensors.

    are_links_outgoing : list of bools
        Used in symmetric tensors only: direction of link in tensor.
        Length is same as rank of tensor.
        Default of `None` will raise exception.

    base_tensor_cls : valid dense quantum tea tensor or `None`
        Used in symmetric tensors only: class representing dense tensor
        Default to :class:`QteaTensor`

    dtype : data type, optional

    device : device specification, optional

    requires_grad: specification if requires an autograd function, not supported here
        Default do None
    """

    has_symmetry = True
    extension = "ast"

    # pylint: disable-next=unused-argument
    def __init__(
        self,
        links,
        ctrl="N",
        are_links_outgoing=None,
        base_tensor_cls=QteaTensor,
        dtype=None,
        device=None,
        requires_grad=None,
    ):
        if requires_grad is not None:
            raise ValueError("Autograd not supported")
        if links:
            self.sym = links[0].sym
            if len(self.sym) > 1 and (not ENABLE_MULTIPLE_SYM):
                raise QRedTeaAbelianSymError("More than one symmetry not yet enabled.")
        else:
            self.sym = None
        self.links = links
        self._are_links_outgoing = are_links_outgoing
        self._base_tensor_cls = base_tensor_cls

        if ctrl == "N":
            self.cs = CouplingSectors(izeros((0, len(links))))
            self.degeneracy_tensors = []
        elif ctrl in ["R", "random", "Z", "O", "1"]:
            if dtype is None:
                # Abelian tensor avoids dependency to explicit data type
                # definitions, retrieve from base tensor
                dummy = base_tensor_cls([1], ctrl=ctrl)
                dtype = dummy.dtype

            cs_ranges = []
            dim = 1
            for link in self.links:
                nn = len(link.irrep_listing)
                dim *= nn
                cs_ranges.append(range(nn))

            cs = indarray([dim, len(self.links)])
            self.degeneracy_tensors = []
            kk = 0
            for elem in itertools.product(*cs_ranges):
                if not self._is_valid_cs(elem):
                    continue

                cs[kk, :] = elem

                # Collect tensor dimensions
                shape = []
                for jj, link_jj in enumerate(self.links):
                    shape.append(link_jj.irrep_listing.degeneracies[elem[jj]])

                tensor = base_tensor_cls(shape, ctrl=ctrl, device=device, dtype=dtype)
                self.degeneracy_tensors.append(tensor)
                kk += 1

            cs = cs[:kk, :]
            self.cs = CouplingSectors(cs, sorted_for=list(range(self.ndim)))
        else:
            raise QRedTeaError(f"There will be no cs etc.: ctrl = {ctrl}).")

        if self._are_links_outgoing is None:
            raise QRedTeaLinkError("Need link directions.")

        self.sanity_check()

    def mpi_send(self, to_, comm, tn_mpi_types):
        """MPI send method. To be implemented."""
        raise NotImplementedError("Not yet implemented.")

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    def are_links_outgoing(self):
        """Define property of outgoing links as property (always False)."""
        return self._are_links_outgoing

    @property
    def base_tensor_cls(self):
        """Base tensor class."""
        return self._base_tensor_cls

    @property
    def device(self):
        """Device where the tensor is stored."""
        for elem in self.degeneracy_tensors:
            return elem.device

        return None

    @property
    def dtype(self):
        """Data type of the underlying arrays."""
        for elem in self.degeneracy_tensors:
            return elem.dtype

        return None

    @property
    def dtype_eps(self):
        """Data type's machine precision of the underlying arrays."""
        for elem in self.degeneracy_tensors:
            return elem.dtype_eps

        return None

    @property
    def ndim(self):
        """Rank of the tensor."""
        return len(self.links)

    @property
    def shape(self):
        """Dimension of tensor along each dimension."""
        return [self.links[ii].shape for ii in range(self.ndim)]

    @property
    def linear_algebra_library(self):
        """Specification of the linear algebra library used as string `numpy-cupy``."""
        if len(self.degeneracy_tensors) == 0:
            raise QRedTeaEmptyTensorError("Running query on empty tensor.")

        return self.degeneracy_tensors[0].linear_algebra_library

    @property
    def links(self):
        """Returns list of :class:`AbelianSymLink` instances."""
        return self._links

    @links.setter
    def links(self, value):
        """Setter for links."""
        self._links = value

    # --------------------------------------------------------------------------
    #                          Overwritten operators
    # --------------------------------------------------------------------------
    #
    # inherit def __eq__
    # inherit def __ne__

    def __add__(self, other):
        """
        Addition of a scalar to a tensor adds it to all the entries.
        If other is another tensor, elementwise addition if they have the same shape
        """
        tmp = self.copy()
        return tmp.add_update(other)

    def __iadd__(self, other):
        """In-place addition of tensor with tensor or scalar (update)."""
        return self.add_update(other)

    def __mul__(self, sc):
        """Multiplication of tensor with scalar returning new tensor as result."""
        new_tensor = deepcopy(self)
        for elem in new_tensor.degeneracy_tensors:
            elem *= sc
        return new_tensor

    def __imul__(self, sc):
        """In-place multiplication of tensor with scalar (update)."""
        for elem in self.degeneracy_tensors:
            elem *= sc
        return self

    def __itruediv__(self, sc):
        """In-place division of tensor with scalar (update)."""
        for elem in self.degeneracy_tensors:
            elem /= sc
        return self

    def __sub__(self, other):
        """
        Subtraction of a scalar to a tensor subtracts it to all the entries.
        If other is another tensor, elementwise subtraction if they have the same shape
        """
        new_tensor = self.copy()
        if isinstance(other, QteaAbelianTensor):
            # Use add_update here as logic is complicated
            new_tensor.add_update(other, factor_other=-1.0)
        else:
            # Raising error even for scalars, while subtracting scalars
            # on a dense tensor is no problem, it is on a sparse tensor
            # if blocks with zeros are compressed away. We would need
            # to ensure all coupling sectors are present and subtract then.
            raise TypeError(
                "Subtraction for QteaAbelianTensor is defined only for"
                + f" QteaAbelianTensor, not {type(other)} (including scalars)."
            )
        return new_tensor

    def __neg__(self):
        """Negative of a tensor returned as a new tensor."""
        new_tensor = QteaAbelianTensor(
            self.links.copy(),
            are_links_outgoing=self._are_links_outgoing.copy(),
            device=self.device,
            dtype=self.dtype,
            base_tensor_cls=self.base_tensor_cls,
        )

        cs = deepcopy(self.cs.denormalized_sectors)
        deg_tensors = []

        for elem in self.degeneracy_tensors:
            deg_tensors.append(-elem)

        new_tensor._append_cs(deg_tensors, cs)

        return new_tensor

    # --------------------------------------------------------------------------
    #                       classmethod, classmethod like
    # --------------------------------------------------------------------------

    @staticmethod
    def convert_operator_dict(
        op_dict, symmetries=None, generators=None, base_tensor_cls=QteaTensor
    ):
        """Convert an operators dict from base tensors to symmetric tensors."""
        if symmetries is None:
            symmetries = []
        if generators is None:
            generators = []

        if len(symmetries) != len(generators):
            print("Error information", symmetries, generators)
            raise QRedTeaAbelianSymError("Generator and symmetry lengths do not match.")

        device_dict = {}

        # pylint: disable-next=dangerous-default-value
        def transform(key, op, device_dict=device_dict):
            device_dict[key] = op.device
            op.convert(None, "cpu")

            if op.ndim == 4:
                op.remove_dummy_link(3)
                op.remove_dummy_link(0)

            return op

        tmp_op = op_dict.transform(transform)

        if len(symmetries) == 0:
            # Define a trivial symmetry (Symmetries and generators at equal length)
            warnings.warn("Defining trivial symmetry to run with symmetric tensors.")
            symmetries = AbelianSymCombinedGroup(AbelianSymU1())
            key = "_auto_generator_zeros" + str(id(symmetries))
            generators = [key]

            for elem in tmp_op.set_names:
                tens = tmp_op[(elem, "id")] * 0.0
                op_dict.ops[(elem, key)] = tens

        strides_dict, inds_dict, link_dict = {}, {}, {}
        for name in tmp_op.set_names:
            strides, inds, link = QteaAbelianTensor._parse_generators(
                tmp_op._ops_dicts[name], symmetries, generators
            )

            strides_dict[name] = strides
            inds_dict[name] = inds
            link_dict[name] = link

        # pylint: disable-next=dangerous-default-value,function-redefined
        def transform(
            key,
            op,
            strides_dict=strides_dict,
            inds_dict=inds_dict,
            link_dict=link_dict,
            generators=generators,
            device_dict=device_dict,
        ):
            # Skipping conversion not an option in `TNOperators.transform()`
            norm = op.norm()
            if (key[1] in generators) and (norm == 0):
                return None
            #    continue

            key0 = key[0]
            tensor = QteaAbelianTensor._from_base_tensor(
                op,
                inds_dict[key0],
                strides_dict[key0],
                link_dict[key0],
                base_tensor_cls,
            )

            tensor.convert(None, device_dict[key])
            return tensor

        return tmp_op.transform(transform)

    def copy(self, dtype=None, device=None):
        """Make a copy of a tensor."""
        if dtype is None:
            dtype = self.dtype
        if device is None:
            device = self.device

        # Links are (almost) immutable, no need to copy
        new_tensor = QteaAbelianTensor(
            self.links.copy(),
            are_links_outgoing=self._are_links_outgoing.copy(),
            device=device,
            dtype=dtype,
            base_tensor_cls=self.base_tensor_cls,
        )

        cs = deepcopy(self.cs.denormalized_sectors)
        deg_tensors = []

        for elem in self.degeneracy_tensors:
            deg_tensors.append(elem.copy())

        new_tensor._append_cs(deg_tensors, cs)

        return new_tensor

    def eye_like(self, link):
        """
        Generate identity matrix.

        **Arguments**

        self : instance of :class:`QteaTensor`
            Extract data type etc from this one here.

        link : same as returned by `links` property, here `AbelianSymLink`.
            Dimension of the square, identity matrix.
        """
        eye = QteaAbelianTensor(
            [link, link],
            ctrl="Z",
            are_links_outgoing=[False, True],
            base_tensor_cls=self.base_tensor_cls,
            dtype=self.dtype,
            device=self.device,
        )

        for ii, cs in eye.cs.iter_sectors():
            if cs[0] != cs[1]:
                # Not a diagonal element
                continue
            dim = eye.degeneracy_tensors[ii].shape[0]
            eye_ii = eye.degeneracy_tensors[ii].eye_like(dim)
            eye.degeneracy_tensors[ii] = eye_ii

        # pylint: disable-next=protected-access
        eye._compress()

        return eye

    def random_unitary(self, links):
        """Generate a random unitary matrix via performing a SVD on a
        random tensor, where a matrix dimension is specified with
        `links`."""

        nn = len(links)
        rand_links = links + links
        are_links_outgoing = [False] * nn + [True] * nn

        rand_mat = QteaAbelianTensor(
            rand_links,
            ctrl="R",
            are_links_outgoing=are_links_outgoing,
            base_tensor_cls=self.base_tensor_cls,
            dtype=self.dtype,
            device=self.device,
        )

        if nn == 1:
            umat, _ = rand_mat.split_qr([0], [1])
            return umat

        # Rank-3 tensors: would have to split one symmetric leg into to links
        # which is not trivial. I suspect we have to take the R-tensor and
        # manually set it to identities and re-contract it as "easiest" way
        # to get a unitary.
        raise NotImplementedError("QR will not preserve tensor rank.")

    def randomize(self, noise=None):
        """
        Randomizes the entries of self.
        Preserves the structure of symmetry blocks.

        **Arguments**

        noise : float | None
            The amount of noise added. None randomizes completely.
        """
        for tens in self.degeneracy_tensors:
            tens.randomize(noise=noise)

    @classmethod
    def read(cls, filehandle, dtype, device, base_tensor_cls, cmplx=True, order="F"):
        """Read a tensor from file."""
        raise NotImplementedError("Cannot read symmetric tensors yet.")

    @classmethod
    def read_pickle(cls, filename):
        """
        Read via pickle module.

        **Arguments**

        filename : str or similar
            File where tensor is stored.

        **Returns**

        :class:`QteaAbelianTensor`
             Tensor from file.
        """
        ext = "pkl" + cls.extension
        if not filename.endswith(ext):
            raise ValueError(
                f"Filename {filename} not valid, extension should be {ext}."
            )

        with open(filename, "rb") as fh:
            obj = pickle.load(fh)

        if not isinstance(obj, cls):
            raise TypeError(f"Loading wrong tensor: {type(obj)} vs {cls}.")

        return obj

    @staticmethod
    def dummy_link(example_link):
        """Generate a dummy link with the identical irreps."""
        irreps = example_link.sym.identical_irrep
        irreps = irreps.reshape([1] + [len(irreps)])
        degs = iones([1])
        irreps_listing = IrrepListing.from_irreps(example_link.sym, irreps, degs)
        return AbelianSymLink(example_link.sym, irreps_listing)

    @staticmethod
    def set_missing_link(links, max_dim, are_links_outgoing=None):
        """
        Calculate the property of a missing link in a list.

        **Arguments**

        links : list of instances of :class:`AbelianSymLink`
            Contains data like returned by property `links`, except
            for one element being `None`

        max_dim : int
            Maximal dimension of link allowed by convergence parameters
            or similar.

        are_links_outgoing : list of bools
            Indicates link direction for symmetry (required here)
        """

        if are_links_outgoing is None:
            raise QRedTeaLinkError("Symmetric tensors require link direction.")

        link = None
        idx = None

        for ii, elem in enumerate(links):
            if elem is None:
                idx = ii
            elif link is None:
                link = elem
                invert_left = are_links_outgoing[ii]
            else:
                invert_right = are_links_outgoing[ii]
                link = link.product_couple(elem, invert_left, invert_right)
                invert_left = False

        if max_dim is None:
            # Nothing to-do, calling method does not restrict bond dimension
            pass
        elif max_dim < link.shape:
            link, _ = link._random_reduce(max_dim)

        links[idx] = link

        return links

    def zeros_like(self):
        """Get a tensor with the same links as `self` but filled with zeros."""
        tens = deepcopy(self)
        tens *= 0.0
        return tens

    # --------------------------------------------------------------------------
    #                            Checks and asserts
    # --------------------------------------------------------------------------
    #
    # inherit def assert_normalized

    def assert_unitary(self, links, tol=1e-7):
        """Raise error if tensor is not unitary up to tolerance for given links."""
        ctensor = self.tensordot(self.conj(), (links, links))

        check_ok = True
        for ii, cs in ctensor.cs.iter_sectors():
            # for diagonal blocks assert identity
            if (cs[: ctensor.ndim // 2] == cs[ctensor.ndim // 2 :]).all():
                # fuse the second half of the links
                ctensor.degeneracy_tensors[ii].fuse_links_update(
                    fuse_low=ctensor.ndim // 2, fuse_high=ctensor.ndim
                )
                # fuse the first half of the links
                ctensor.degeneracy_tensors[ii].fuse_links_update(
                    fuse_low=0, fuse_high=-1 + ctensor.ndim // 2
                )
                # the result should be compared to a rank-2 identity
                ctensor.degeneracy_tensors[ii].assert_identity(tol=tol)

            # for off-diagonal assert that the blocks are zero
            else:
                check_ok = ctensor.degeneracy_tensors[ii].norm() < tol

            if not check_ok:
                raise QRedTeaError("Tensor not unitary! Problem in off-diagonal block.")

    def are_equal(self, other, tol=1e-7):
        """Check if two tensors are equal."""
        if self.ndim != other.ndim:
            return False

        for ii, link in enumerate(self.links):
            if link != other.links[ii]:
                return False

        for ii, outgoing in enumerate(self._are_links_outgoing):
            if outgoing != other.are_links_outgoing[ii]:
                return False

        # Generate hash table for all links
        self.cs.generate_hashes(tuple(range(self.ndim)))

        are_equal = True
        for ii, elem in other.cs.iter_sectors():
            jj_list = self.cs[tuple(elem)]

            if len(jj_list) > 1:
                raise QRedTeaAbelianSymError(
                    "Hashing all links should not lead to list"
                )

            jj = jj_list[0]

            if jj is None:
                # There is a coupling sector in other, which is not in self
                are_equal = False
                break

            deg_tensors_equal = self.degeneracy_tensors[jj].are_equal(
                other.degeneracy_tensors[ii], tol=tol
            )

            if not deg_tensors_equal:
                are_equal = False
                break

        if not are_equal:
            return False

        for _, _ in self.cs.iter_tracker_false():
            # There is a CS in self which was not in other
            return False

        return True

    def assert_identity(self, tol=1e-7):
        """Check if tensor is an identity matrix."""
        if self.ndim != 2:
            raise QRedTeaRankError("Not a matrix, hence not the identity.")

        if self.links[0] != self.links[1]:
            raise QRedTeaLinkError("Links different, cannot be identity.")

        if self._are_links_outgoing[0] == self._are_links_outgoing[1]:
            raise QRedTeaLinkError(
                "Directions are not different, but condition for identity."
            )

        for ii, cs_ii in self.cs.iter_sectors():
            elem = self.degeneracy_tensors[ii]
            try:
                elem.assert_identity(tol=tol)
            except:
                print(
                    "Additional information",
                    cs_ii,
                    self.links[0].irrep_listing.irreps[cs_ii[0], :],
                    self.links[0].irrep_listing.irreps[cs_ii[1], :],
                )
                raise

    def is_close_identity(self, tol=1e-7):
        """Check i rank-2 tensor is close to identity."""
        raise NotImplementedError("Easy, but not needed yet.")

    def is_dtype_complex(self):
        """Check if data type is complex."""
        if len(self.degeneracy_tensors) == 0:
            raise QRedTeaEmptyTensorError("Running check on empty tensor.")

        return self.degeneracy_tensors[0].is_dtype_complex()

    def is_implemented_device(self, query):
        """
        Check if argument query is an implemented device via base tensor.

        Parameters
        ----------

        query : str
            String to be tested if it corresponds to a device
            implemented with this tensor.

        Returns
        -------

        is_implemented : bool
            True if string is available as device.
        """
        for elem in self.degeneracy_tensors:
            return elem.is_implemented_device(query)

    def is_identical_irrep(self, link_idx):
        """Assert that specified link is identical irreps."""
        link = self.links[link_idx]
        identical = link.create_dummy(link.sym)

        return link == identical

    def is_link_full(self, link_idx):
        """Check if the link at the given index is at full bond dimension."""
        links = self.links.copy()
        links[link_idx] = None

        links = self.set_missing_link(
            links, None, are_links_outgoing=self.are_links_outgoing
        )

        return self.links[link_idx].shape >= links[link_idx].shape

    def sanity_check(self):
        """Quick set of checks for tensor."""
        if not RUN_SANITY_CHECKS:
            return

        if len(self._are_links_outgoing) != len(self.links):
            raise QRedTeaLinkError("Mismatch lengths.")

        if len(self.degeneracy_tensors) != self.cs.num_coupling_sectors:
            raise QRedTeaAbelianSymError("Mismatch len coupling sectors.")

        for link in self.links:
            link.sanity_check()

        self.cs.sanity_check()

        for ii, elem in self.cs.iter_sectors():
            if not self._is_valid_cs(elem):
                raise QRedTeaAbelianSymError("CS not valid")

        for ii in range(self.ndim):
            for jj, kk in enumerate(self.cs.denormalized_sectors[:, ii]):
                deg_t = self.degeneracy_tensors[jj].shape
                deg_l = self.links[ii].irrep_listing.degeneracies[kk]

                if deg_t[ii] != deg_l:
                    print("Error information cs", kk)
                    print("Error information (tens/idx/link)", deg_t, ii, deg_l)
                    raise QRedTeaAbelianSymError("Mismatch degeneracy tensor and link.")

    # --------------------------------------------------------------------------
    #                       Single-tensor operations
    # --------------------------------------------------------------------------

    def attach_dummy_link(self, position, is_outgoing=True):
        """Attach dummy link at given position (inplace update)."""

        dummy = self.links[0].create_dummy(self.links[0].sym)

        self.links.insert(position, dummy)
        self._are_links_outgoing.insert(position, is_outgoing)
        self.cs.attach_dummy_link(position)

        for elem in self.degeneracy_tensors:
            elem.attach_dummy_link(position)

        return self

    def conj(self):
        """Return the complex conjugated in a new tensor."""
        new_tensor = QteaAbelianTensor(
            self.links.copy(),
            are_links_outgoing=list(ilogical_not(self._are_links_outgoing)),
            device=self.device,
            dtype=self.dtype,
            base_tensor_cls=self.base_tensor_cls,
        )

        cs = deepcopy(self.cs.denormalized_sectors)
        deg_tensors = []

        for elem in self.degeneracy_tensors:
            deg_tensors.append(elem.conj())

        new_tensor._append_cs(deg_tensors, cs)

        return new_tensor

    def conj_update(self):
        """
        Apply the complex conjugated to the tensor in place
        (including flip directions).
        """
        for elem in self.degeneracy_tensors:
            elem.conj_update()

        self._are_links_outgoing = list(ilogical_not(self._are_links_outgoing))

    def convert(self, dtype=None, device=None, stream=None):
        """Convert underlying array to the specified data type inplace."""
        for elem in self.degeneracy_tensors:
            elem.convert(dtype, device, stream)

        return self

    def convert_singvals(self, singvals, dtype, device):
        """Convert the singular values via a tensor."""
        if len(self.degeneracy_tensors) == 0:
            raise QRedTeaEmptyTensorError("Running on empty tensor.")

        tens = self.degeneracy_tensors[0]

        for ii, elem in enumerate(singvals.link_weights):
            singvals.link_weights[ii] = tens.convert_singvals(elem, dtype, device)

    def dtype_from_char(self, dtype):
        """Resolve data type from chars C, D, S, Z and optionally H."""
        # Have to rely on base tensor here
        for elem in self.degeneracy_tensors:
            return elem.dtype_from_char(dtype)

        return None

    def eig_api(
        self,
        matvec_func,
        links,  # pylint: disable=unused-argument
        conv_params,
        args_func=None,
        kwargs_func=None,
    ):
        """
        Interface to hermitian eigenproblem

        **Arguments**

        matvec_func : callable
            Mulitplies "matrix" with "vector"

        links : links according to :class:`QteaTensor`
            Contain the dimension of the problem.

        conv_params : instance of :class:`TNConvergenceParameters`
            Settings for eigenproblem with Arnoldi method.

        args_func : arguments for matvec_func

        kwargs_func : keyword arguments for matvec_func

        **Returns**

        eigenvalues : scalar

        eigenvectors : instance of :class:`QteaAbelianTensor`
        """
        if len(self.degeneracy_tensors) == 0:
            raise QRedTeaEmptyTensorError("Running eigenproblem on empty tensor.")

        kwargs, linear_operator, eigsh = self.degeneracy_tensors[0].prepare_eig_api(
            conv_params
        )

        use_qtea_solver = kwargs.pop("use_qtea_solver", False)
        injected_funcs = kwargs.pop("injected_funcs", {})

        if not use_qtea_solver:
            mapping = self._mapping_to_vec()
            ham_dim = mapping["dim"]

            condition_a = ham_dim == 1
            condition_b = self.is_dtype_complex() and (ham_dim == 2)

            # Have to overwrite decision - ARPACK has problem with matrices of
            # dimension 1x1 (real) and up to 2x2 (complex)
            use_qtea_solver = condition_a or condition_b

        if not use_qtea_solver:
            # From here on, it is the ARPACK solution
            if args_func is None:
                args_func = []
            if kwargs_func is None:
                kwargs_func = {}

            # pylint: disable-next=dangerous-default-value
            def my_matvec(
                vec,
                func=matvec_func,
                this=self,
                mapping=mapping,
                args=args_func,
                kwargs=kwargs_func,
            ):
                # We assume always incoming vector here
                tens = this._from_vector(vec, mapping)
                tens = -func(tens, *args, **kwargs)
                return tens._to_vector(mapping)

            lin_op = linear_operator(
                (ham_dim, ham_dim), matvec=my_matvec, dtype=self.dtype
            )

            if "v0" in kwargs:
                kwargs["v0"] = self._to_vector(mapping)

            try:
                eigenvalues, eigenvectors = eigsh(lin_op, **kwargs)
                tens = self._from_vector(eigenvectors.flatten(), mapping)

                return -eigenvalues, tens

            except ArpackError:
                pass

            # Try increasing ncv
            ncv_scipy_default = min(ham_dim, max(2 * kwargs["k"] + 1, 20))
            kwargs["ncv"] = min(ham_dim - 1, 4 * ncv_scipy_default)
            warnings.warn("Trying again with Arpack and ncv=%d" % (int(kwargs["ncv"])))

            if "v0" in kwargs:
                kwargs["v0"] = self._to_vector(mapping)

            try:
                eigenvalues, eigenvectors = eigsh(lin_op, **kwargs)
                tens = self._from_vector(eigenvectors.flatten(), mapping)

                return -eigenvalues, tens
            except ArpackError:
                # Forget about ARPACK for this call
                warnings.warn("Switching to Qtea solver.")
                use_qtea_solver = True

        # use_qtea_solver must be True now
        return self.eig_api_qtea(
            matvec_func,
            conv_params,
            args_func=args_func,
            kwargs_func=kwargs_func,
            injected_funcs=injected_funcs,
        )

    def eig_api_qtea(
        self,
        matvec_func,
        conv_params,
        args_func=None,
        kwargs_func=None,
        injected_funcs=None,
    ):
        """Interface to hermitian eigensolver via qtealeaves' solver."""
        solver = EigenSolverH(
            self,
            matvec_func,
            conv_params,
            args_func=args_func,
            kwargs_func=kwargs_func,
            injected_funcs=injected_funcs,
        )

        return solver.solve()

    def einsum(self, einsum_str, *others):
        """
        Call to einsum with `self` as first tensor (not implemented).

        Arguments
        ---------

        einsum_str : str
            Einsum contraction rule.

        others: List[:class:`QteaAbelianTensors`]
            2nd, 3rd, ..., n-th tensor in einsum rule as
            positional arguments.

        Results
        -------

        tensor : :class:`QteaAbelianTensor`
            Contracted tensor according to the einsum rules.

        Details
        -------

        The call ``np.einsum(einsum_str, x.elem, y.elem, z.elem)`` translates
        into ``x.einsum(einsum_str, y, z)`` for x, y, and z being
        :class:`QteaAbelianTensor`.
        """
        if len(others) == 1:
            # Can be deleted once the general implementation is here. It covers only
            #
            # * einsum with two tensors
            # * no batch dimension
            # * no permutation
            # * no special einsum notation like ...

            estr_in, estr_out = einsum_str.split("->")
            estr_self, estr_other = estr_in.split(",")

            c_links_a = []
            c_links_b = []
            default_out = []
            for ii, elem in enumerate(estr_self):
                if (elem in estr_other) and (elem in estr_out):
                    raise NotImplementedError(
                        "Batch dimension in einsum with symmetries."
                    )

                if elem in estr_other:
                    c_links_a.append(ii)
                    c_links_b.append(estr_other.index(elem))
                else:
                    default_out.append(elem)

            for elem in estr_other:
                if elem not in estr_self:
                    default_out.append(elem)

            ctensor = self.tensordot(others[0], (c_links_a, c_links_b))

            default_out = "".join(default_out)
            if default_out != estr_out:
                raise NotImplementedError(
                    "einsum via tensordot + permuation with symmetries."
                )

            return ctensor

        # This implementation is tricky as we have to match coupling sectors
        # of a potential list of tensors
        raise NotImplementedError(
            "einsum and Abelian tensors requires implementation effort."
        )

    def getsizeof(self):
        """Size in memory (approximate, e.g., without considering small meta data)."""
        size = 0
        for elem in self.degeneracy_tensors:
            size += elem.getsizeof()

        return size

    def get_entry(self):
        """Get entry if scalar on host."""
        if iall(self.cs.denormalized_sectors.shape == (1, 0)):
            return self.degeneracy_tensors[0].get_entry()

        if len(self.degeneracy_tensors) == 0:
            return 0.0

        print(
            "Error information",
            self.cs.denormalized_sectors.shape,
            len(self.degeneracy_tensors),
        )
        raise QRedTeaError("`get_entry` can only work on scalars.")

    def flip_links_update(self, link_inds):
        """Flip irreps on given links."""
        irreps = izeros((self.cs.num_coupling_sectors, len(self.links[0].sym)))
        for ii in link_inds:
            irreps[:, :] = self.links[ii].select_irreps(self.cs.get_col(ii))
            irreps[:, :] = self.links[ii].sym.invert_irrep(irreps)

            self.links[ii] = self.links[ii].invert()

            cs, _, inds = self.links[ii].generate_cs(irreps)
            self.cs.denormalized_sectors[inds, ii] = cs

            self._are_links_outgoing[ii] = not self._are_links_outgoing[ii]

        self.cs.sorted_for = None
        self.cs.hashed_for = None

        return self

    def fuse_links_update(self, fuse_low, fuse_high, is_link_outgoing=True):
        """Fuses one set of links to a single link (inplace-update, no unfuse information)."""
        # link, fuse_rule = self._fuse_prepare(fuse_low, fuse_high)

        # ndim = self.ndim - (fuse_high - fuse_low)
        # tracker = {}
        # deg_tensors = []
        # idx = -1
        # cs = indarray((self.cs.num_coupling_sectors, ndim))

        # for ii in range(self.cs_num_coupling_sectors):
        #    key_f = tuple(self.cs_denormalized_sectors[ii, fuse_low : fuse_high + 1])

        #    if key_f not in tracker:
        #        pass

        all_fused_links_dim_one = True
        for link in self.links[fuse_low : fuse_high + 1]:
            all_fused_links_dim_one = all_fused_links_dim_one and link.shape == 1

        if all_fused_links_dim_one:
            return self._trivial_fuse_links(fuse_low, fuse_high, is_link_outgoing)

        raise NotImplementedError("Problem with overwriting CS sectors.")

        # self._trivial_fuse_links(fuse_low, fuse_high, is_link_outgoing)

        # if iproduct(self.shape) >  1000:
        #    warnings.warn("current fuse_links_update approach inefficient for large tensors.")

        # Move links to be fused upfront
        # legs_left = list(range(fuse_low, fuse_high + 1))
        # legs_right = self._invert_link_selection(legs_left)

        # perm = legs_left + legs_right
        # self.transpose_update(perm)

        # for elem in self.degeneracy_tensors:
        #    print("Norm", elem.norm())

        # span_a = len(legs_left)
        # link_a, fuse_rule_forward_a = self._fuse_prepare(0, span_a - 1)

        # Do the same steps as for the QR, just finalize only links_b without
        # every exexuting decomposition
        # split_tens, _, fuse_r = self._split_prepare(legs_left, legs_right)

        # new_tensor = self._split_finalize(
        #    split_tens, 1, legs_right, split_tens, is_link_outgoing, fuse_r
        # )

        # perm = list(range(1, fuse_low + 1)) + [0] + list(range(fuse_low + 1, new_tensor.ndim))
        # new_tensor.transpose_update(perm)

        # self.links = new_tensor.links
        # self._are_links_outgoing = new_tensor.are_links_outgoing
        # self.cs = new_tensor.cs
        # self.degeneracy_tensors = new_tensor.degeneracy_tensors

        # return self

    def norm(self):
        """Calculate the norm of the tensor <tensor|tensor>."""
        if len(self.degeneracy_tensors) == 0:
            return 0.0

        cum_norm = self.degeneracy_tensors[0].norm()

        for elem in self.degeneracy_tensors[1:]:
            cum_norm += elem.norm()

        return cum_norm

    def norm_sqrt(self):
        """Calculate the square root of the norm of the tensor <tensor|tensor>."""
        if len(self.degeneracy_tensors) == 0:
            return 0.0

        norm = self.norm()
        sqrt = self.degeneracy_tensors[0].get_attr("sqrt")

        return sqrt(norm)

    def normalize(self):
        """Normalize tensor with sqrt(<tensor|tensor>)."""
        self /= self.norm_sqrt()

        if RUN_SANITY_CHECKS:
            self.sanity_check()

        return self

    def remove_dummy_link(self, position):
        """Remove the dummy link at given position (inplace update)."""
        if self.shape[position] != 1:
            print("Error information", self.shape, position)
            raise QRedTeaLinkError(
                "Link to be removed as dummy link has not dimension 1."
            )

        link = self.links[position]
        dummy = link.create_dummy(link.sym)
        if link != dummy:
            print(
                "Error information",
                link.irrep_listing.irreps,
                link.irrep_listing.degeneracies,
            )
            raise QRedTeaLinkError(
                "Link to be removed as dummy link is not identical irrep."
            )

        del self.links[position]
        del self._are_links_outgoing[position]

        self.cs.remove_dummy_link(position)

        for elem in self.degeneracy_tensors:
            elem.remove_dummy_link(position)

        return self

    def restrict_irreps(self, link_idx, sector):
        """
        Restrict, i.e., project, link to a sector

        **Arguments**

        link_idx : int
            Restrict, i.e., project out, symmetry sectors on this link.

        sector : irreps
            Irreps to be kept, allows for multiple ones.

        **Returns**

        :class:`QteaAbelianTensor`
            New tensor based on `self` with restricted
            irreps on `link_idx`-th link according to sector.

        **Raises**

        :class:`QRedTeaEmptyTensorError`
            For restricting irreps, we throw an error if an empty
            tensor is generated.
        """
        irreps = self.links[link_idx].irrep_listing.intersection(
            sector, deg_func=imaximum
        )

        link_a = AbelianSymLink(self.sym, irreps)
        link_b = self.links[link_idx]

        dir_a = self.are_links_outgoing[link_idx]
        dir_b = not self.are_links_outgoing[link_idx]

        projector = QteaAbelianTensor(
            [link_a, link_b],
            ctrl="1",
            are_links_outgoing=[dir_a, dir_b],
            base_tensor_cls=self._base_tensor_cls,
            dtype=self.dtype,
            device=self.device,
        )

        tensor = self.tensordot(projector, ([link_idx], [1]))
        perm = _transpose_idx(tensor.ndim, link_idx)
        tensor = tensor.transpose(perm)

        if tensor.cs.num_coupling_sectors == 0:
            raise QRedTeaEmptyTensorError("Created empty tensors.")

        return tensor

    def save_pickle(self, filename):
        """
        Save class via pickle module.

        **Arguments**

        filename : str
            If extension matches, tensor is stored under this filename.
            Otherwise, file extension is added.
        """
        device = self.device
        if device != "cpu":
            # ASsume pickle needs to be on host
            self.convert(None, "cpu")

        ext = "pkl" + self.extension
        if not filename.endswith(ext):
            filename += "." + ext

        with open(filename, "wb+") as fh:
            pickle.dump(self, fh)

    def scale_link(self, link_weights, link_idx):
        """
        Scale tensor along one link at `link_idx` with weights.

        **Arguments**

        link_weights : instance of :class:`AbelianSymLinkWeight`
            Scalar weights, e.g., singular values.

        link_idx : int
            Link which should be scaled.

        **Returns**

        updated_link : instance of :class:`QteaTensor`
        """
        tensor = self._empty_from_links_directions(
            self.links, self._are_links_outgoing, self.base_tensor_cls
        )

        cs = self.cs.denormalized_sectors.copy()
        deg_tensors = []
        for elem in self.degeneracy_tensors:
            deg_tensors.append(elem.copy())

        tensor._append_cs(deg_tensors, cs)
        tensor.scale_link_update(link_weights, link_idx)

        return tensor

    def scale_link_update(self, link_weights, link_idx):
        """
        Scale tensor along one link at `link_idx` with weights (inplace update).

        **Arguments**

        link_weights : instance of :class:`AbelianSymLinkWeight`
            Scalar weights, e.g., singular values.

        link_idx : int
            Link which should be scaled.
        """

        if (link_idx < 0) or (link_idx >= self.ndim):
            raise QRedTeaLinkError("Link index error")

        tmp_link = link_weights.link
        has_link_mismatch = self.links[link_idx] != tmp_link
        if has_link_mismatch:
            print(
                "Error information tensor-link",
                link_idx,
                self.links[link_idx].irrep_listing.irreps,
                self.links[link_idx].irrep_listing.degeneracies,
            )
            print(
                "Error information link weights",
                link_idx,
                link_weights.link.irrep_listing.irreps,
                link_weights.link.irrep_listing.degeneracies,
            )
            print(
                "Error information link weights",
                link_idx,
                tmp_link.irrep_listing.irreps,
                tmp_link.irrep_listing.degeneracies,
            )

            raise QRedTeaLinkError("Non-matching links.")

        if len(self.degeneracy_tensors) == 0:
            # Nothing to scale
            return self

        if len(link_weights) == 0:
            # Scaling with zeros (smarter way to do that, but working for now)
            self *= 0
            return self

        link_weights.generate_hashes()

        for ii, elem in self.cs.iter_sectors():
            key = (elem[link_idx],)
            vec = link_weights[key]

            self.degeneracy_tensors[ii].scale_link_update(vec, link_idx)

        if len(self.degeneracy_tensors) != self.cs.num_coupling_sectors:
            raise QRedTeaAbelianSymError("Mismatch cs and deg-tensor length.")

        if self.cs.num_coupling_sectors == 0:
            raise QRedTeaEmptyTensorError("Created empty tensors.")

        return self

    def set_diagonal_entry(self, position, value):
        """Set the diagonal element in a rank-2 tensor (inplace update)"""
        raise NotImplementedError(
            "Requires to scan irreps degeneracies for being meaningful."
        )

    def set_matrix_entry(self, idx_row, idx_col, value):
        """Set one element in a rank-2 tensor (inplace update)"""
        raise NotImplementedError(
            "Requires to scan irreps degeneracies for being meaningful."
        )

    def split_link_deg_charge(self, link_idx):
        """
        Split a link into two, where one carries the degeneracy, the other the charge.
        Documentation see :class:`_AbstractQteaTensor`.
        """
        link = self.links[link_idx]
        mapping = {}
        j2 = 0
        for jj, deg_jj in enumerate(link.irrep_listing.degeneracies):
            j1 = j2
            j2 += deg_jj
            mapping[jj] = (j1, j2)

        degeneracy_tensors = []
        # for elem in self.degeneracy_tensors:
        for ii, cs_ii in self.cs.iter_sectors():
            elem = self.degeneracy_tensors[ii]
            shape = list(elem.shape)
            shape_a = shape[:link_idx] + [j2] + shape[link_idx + 1 :]
            shape_b = shape[:link_idx] + [j2, 1] + shape[link_idx + 1 :]
            tensor = self.base_tensor_cls(shape_a, dtype=self.dtype, device=self.device)

            corner_low = [0] * len(shape)
            corner_high = list(shape)
            i1, i2 = mapping[cs_ii[link_idx]]
            corner_low[link_idx] = i1
            corner_high[link_idx] = i2

            tensor.set_subtensor_entry(corner_low, corner_high, elem)
            tensor = tensor.reshape(shape_b)
            degeneracy_tensors.append(tensor)

        # Prepare links
        links = self.links[:link_idx] + [None, None] + self.links[link_idx + 1 :]

        sym = self.links[link_idx].sym
        irrep_deg = sym.identical_irrep
        irrep_deg = np.reshape(irrep_deg, [1, irrep_deg.shape[0]])
        degs = j2 * iones(1)
        irrep_a = IrrepListing.from_irreps(sym, irrep_deg, degs)
        link_a = AbelianSymLink(sym, irrep_a)

        irrep_charge = self.links[link_idx].irrep_listing.irreps
        degs = iones(len(irrep_charge))
        irrep_b = IrrepListing.from_irreps(sym, irrep_charge, degs)
        link_b = AbelianSymLink(sym, irrep_b)

        links[link_idx] = link_a
        links[link_idx + 1] = link_b

        are_links_outgoing = (
            self.are_links_outgoing[: link_idx + 1] + self.are_links_outgoing[link_idx:]
        )

        cs_old = deepcopy(self.cs.denormalized_sectors)
        cs = izeros([cs_old.shape[0], cs_old.shape[1] + 1])
        cs[:, :link_idx] = cs_old[:, :link_idx]
        cs[:, link_idx + 1 :] = cs_old[:, link_idx:]

        new_tensor = QteaAbelianTensor(
            links,
            are_links_outgoing=are_links_outgoing,
            base_tensor_cls=self.base_tensor_cls,
        )

        new_tensor._append_cs(degeneracy_tensors, cs)

        return new_tensor

    # pylint: disable-next=unused-argument
    def to_dense(self, true_copy=False):
        """Return dense tensor (if `true_copy=False`, same object may be returned)."""

        # Construct mappings where mappings[ii][jj] return the sub-matrix indices for
        # the ii-th link and the jj-th irrep.
        mappings = []
        for link in self.links:
            mappings.append({})

            j2 = 0
            for jj, deg_jj in enumerate(link.irrep_listing.degeneracies):
                j1 = j2
                j2 += deg_jj

                mappings[-1][jj] = (j1, j2)

        shape = self.shape

        dense = self.base_tensor_cls(shape, dtype=self.dtype, device=self.device)
        for ii, cs_ii in self.cs.iter_sectors():
            corner_low = []
            corner_high = []

            for jj, cs_ii_jj in enumerate(cs_ii):
                corners = mappings[jj][cs_ii_jj]
                corner_low.append(corners[0])
                corner_high.append(corners[1])

            deg_tensor = self.degeneracy_tensors[ii]
            dense.set_subtensor_entry(corner_low, corner_high, deg_tensor)

        return dense

    # pylint: disable-next=unused-argument
    def to_dense_singvals(self, s_vals, true_copy=False):
        """Convert singular values to dense vector without symmetries."""
        mapping = {}
        j2 = 0
        for jj, deg_jj in enumerate(s_vals.link.irrep_listing.degeneracies):
            j1 = j2
            j2 += deg_jj

            mapping[jj] = (j1, j2)

        shape = s_vals.link.shape

        # Line will break for any non-numpy backend
        # pylint: disable-next=not-callable
        dtype = self.dtype.type(0).real.dtype
        dense_s_vals = self.degeneracy_tensors[0].vector_with_dim_like(
            shape, dtype=dtype
        )

        for ii, cs_ii in enumerate(s_vals.cs.denormalized_sectors):
            j1, j2 = mapping[int(cs_ii)]

            dense_s_vals[j1:j2] = s_vals.link_weights[ii]

        return dense_s_vals

    def trace(self, return_real_part=False, do_get=False):
        """Take the trace of a rank-2 tensor."""
        if self.ndim != 2:
            raise QRedTeaRankError("Can only run on rank-2 tensor.")

        if self._are_links_outgoing[0] == self._are_links_outgoing[1]:
            raise QRedTeaLinkError("Link directions have to be different.")

        if self.links[0] != self.links[1]:
            raise QRedTeaLinkError("Links have to match.")

        if len(self.degeneracy_tensors) == 0:
            # Running on tensor without coupling sectors
            return 0.0

        values = []
        for ii, elem in self.cs.iter_sectors():
            if elem[0] != elem[1]:
                continue

            tens = self.degeneracy_tensors[ii]
            values.append(tens.trace(return_real_part, do_get))

        if len(values) == 0:
            return 0.0

        value = values[0]
        for elem in values[1:]:
            value += elem

        return value

    def trace_one_dim_pair(self, links):
        """Trace a pair of links with dimenion one. Inplace update."""
        if len(links) != 2:
            raise QRedTeaLinkError("Can only run on pair of links")

        ii = min(links[0], links[1])
        jj = max(links[1], links[0])

        if ii == jj:
            raise QRedTeaLinkError("Same link.")

        if self._are_links_outgoing[ii] == self._are_links_outgoing[jj]:
            raise QRedTeaLinkError("Mismatch link directions.")

        if self.links[ii] != self.links[jj]:
            raise QRedTeaLinkError("Mismtach links.")

        if self.links[ii].shape != 1:
            raise QRedTeaLinkError("First link not one-dimensional.")

        if self.links[jj].shape != 1:
            raise QRedTeaLinkError("Second link not one-dimensional.")

        del self.links[jj]
        del self.links[ii]

        del self._are_links_outgoing[jj]
        del self._are_links_outgoing[ii]

        # Checks here should not be good enough to realize it is not a true
        # dummy link of the identical irrep
        self.cs.remove_dummy_link(jj)
        self.cs.remove_dummy_link(ii)

        for elem in self.degeneracy_tensors:
            elem.remove_dummy_link(jj)
            elem.remove_dummy_link(ii)

        return self

    def transpose(self, permutation):
        """Permute the links of the tensor and return new tensor."""
        transposed = deepcopy(self)
        # transposed.links = transposed.links[permutation]
        transposed.links = [
            transposed.links[permutation[ii]] for ii in range(self.ndim)
        ]
        # transposed.are_links_outgoing = transposed.are_links_outgoing[permutation]
        transposed._are_links_outgoing = [
            transposed.are_links_outgoing[permutation[ii]] for ii in range(self.ndim)
        ]
        transposed.cs = transposed.cs.transpose(permutation)

        for elem in transposed.degeneracy_tensors:
            elem.transpose_update(permutation)

        return transposed

    def transpose_update(self, permutation):
        """Permute the links of the tensor inplace."""
        self.links = [self.links[ii] for ii in permutation]
        self._are_links_outgoing = [self._are_links_outgoing[ii] for ii in permutation]
        self.cs = self.cs.transpose(permutation)

        for elem in self.degeneracy_tensors:
            elem.transpose_update(permutation)

        return self

    def write(self, filehandle, cmplx=None):
        """Write tensor in original Fortran compatible way."""
        raise NotImplementedError("Cannot write symmetric tensors yet.")

    # --------------------------------------------------------------------------
    #                         Two-tensor operations
    # --------------------------------------------------------------------------

    def add_update(self, other, factor_this=None, factor_other=None):
        """
        Inplace addition as `self = factor_this * self + factor_other * other`.
        """
        if self.ndim != other.ndim:
            raise QRedTeaRankError("Different number of links.")

        for ii in range(self.ndim):
            if self._are_links_outgoing[ii] != other.are_links_outgoing[ii]:
                print("Error information self", self.shape, self._are_links_outgoing)
                print("Error information other", other.shape, other.are_links_outgoing)
                raise QRedTeaLinkError(f"Direction link {ii} not matching.")

            if self.links[ii] != other.links[ii]:
                print("Error information self", self.shape, self._are_links_outgoing)
                print("Error information other", other.shape, other.are_links_outgoing)
                raise QRedTeaLinkError(f"Link {ii} not matching.")

        if len(other.degeneracy_tensors) == 0:
            # Quick return - scale at worst case
            if factor_this is not None:
                self *= factor_this

            return self

        if len(self.degeneracy_tensors) == 0:
            # Quick return - copy and scale at worst case
            self._append_cs(
                deepcopy(other.degeneracy_tensors), other.cs.denormalized_sectors
            )

            if factor_other is not None:
                self *= factor_other

            return self

        links = tuple(range(self.ndim))

        self.cs.generate_hashes(links)

        unmatched_this = [False] * len(self.degeneracy_tensors)
        unmatched = []
        for ii, elem in other.cs.iter_sectors():
            jj_list = self.cs[tuple(elem)]

            if len(jj_list) > 1:
                raise QRedTeaAbelianSymError(
                    "Hashing all links should not lead to list."
                )

            jj = jj_list[0]

            if jj is None:
                unmatched.append(ii)
                continue

            if unmatched_this[jj]:
                raise QRedTeaAbelianSymError("Accessing same degeneracy tensor twice.")
            unmatched_this[jj] = True

            # Execute update
            self.degeneracy_tensors[jj].add_update(
                other.degeneracy_tensors[ii],
                factor_this=factor_this,
                factor_other=factor_other,
            )

        if factor_this is not None:
            # If there was no match for a degeneracy tensor in self in other,
            # it has not been multiplied with factor_this yet
            for jj, flag_this in enumerate(unmatched_this):
                if not flag_this:
                    self.degeneracy_tensors[jj] *= factor_this

        if len(unmatched) == 0:
            # There are no unmatched CS appearing in other, but not in self
            return self

        num_cs_a = self.cs.num_coupling_sectors
        num_cs_b = len(unmatched)

        num_cs = num_cs_a + num_cs_b

        cs = indarray((num_cs, self.ndim))
        cs[:num_cs_a, :] = self.cs.denormalized_sectors
        cs[num_cs_a:, :] = other.cs.denormalized_sectors[unmatched, :]

        self.cs = CouplingSectors(cs)

        for ii in unmatched:
            self.degeneracy_tensors.append(other.degeneracy_tensors[ii])

            if factor_other is not None:
                self.degeneracy_tensors[-1] *= factor_other

        return self

    def dot(self, other):
        """Inner product of two tensors <self|other>."""
        # The easy way out is using tensordot
        if self.ndim != other.ndim:
            raise QRedTeaRankError("Cannot use dot on tensors with unequal rank.")

        cidx = list(range(self.ndim))
        bra = self.conj()
        tmp = bra.tensordot(other, (cidx, cidx))

        if len(tmp.degeneracy_tensors) == 0:
            return 0.0

        return tmp.degeneracy_tensors[0].flatten()

    def expand_link_tensorpair(self, other, link_self, link_other, new_dim):
        """
        Expand randomly the link between a pair of tensors.

        **Arguments**

        other : instance of :class`QteaAbelianTensor`

        link_self : int
            Expand this link in `self`

        link_other : int
            Expand this link in `other`. Link must be a match (dimension etc.)

        **Returns**

        new_this : instance of :class`QteaAbelianTensor`
            Expanded version of `self`

        new_other : instance of :class`QteaAbelianTensor`
            Expanded version of `other`
        """
        if self.links[link_self] != other.links[link_other]:
            raise QRedTeaLinkError("Links connecting tensor pair are not equal.")

        link_inds_comb_a = self._invert_link_selection([link_self])
        link_inds_comb_b = other._invert_link_selection([link_other])

        links_comb_a = [self.links[ii] for ii in link_inds_comb_a]
        links_comb_b = [other.links[ii] for ii in link_inds_comb_b]

        # The "not" for out_comb_x is by intuition for now (dj)
        if self.are_links_outgoing[link_self]:
            out_comb_a = [self._are_links_outgoing[ii] for ii in link_inds_comb_a]
            out_comb_b = [not other.are_links_outgoing[ii] for ii in link_inds_comb_b]
        else:
            out_comb_a = [not self._are_links_outgoing[ii] for ii in link_inds_comb_a]
            out_comb_b = [other.are_links_outgoing[ii] for ii in link_inds_comb_b]

        link_comb_a = AbelianSymLink.from_link_list(
            links_comb_a, are_links_outgoing=out_comb_a
        )
        link_comb_b = AbelianSymLink.from_link_list(
            links_comb_b, are_links_outgoing=out_comb_b
        )

        link_intersection = link_comb_a.intersection(link_comb_b)
        link_intersection_orig = self.links[link_self].intersection(
            other.links[link_other]
        )

        if link_intersection.shape < link_intersection_orig.shape:
            warnings.warn("Intersection link lists < intersection links.")

            # link_intersection.print_full(label="intersect")
            # link_intersection_orig.print_full(label="intersect orig")
            # self.links[link_self].print_full(label="self link")
            # other.links[link_other].print_full(label="other link")
            # link_comb_a.print_full(label="comb_a")
            # link_comb_b.print_full(label="comb_b")

            # print(
            #    "Intersection smaller than link.",
            #    link_intersection.shape,
            #    link_intersection_orig.shape,
            #    self.links[link_self].shape,
            #    other.links[link_other].shape,
            # )
            # raise QRedTeaAbelianSymError("Problem with building intersection.")

        if link_intersection.shape < self.links[link_self].shape:
            # Can happen after initialization when sectors where truncated
            # at top link
            print(
                "Intersection smaller than link.",
                link_intersection.shape,
                link_intersection_orig.shape,
                self.links[link_self].shape,
                other.links[link_other].shape,
            )
            return self, other
            # print("Error information", link_intersection.shape, self.links[link_self].shape)
            # raise QRedTeaAbelianSymError("Problem building intersection.")

        current_dim = self.links[link_self].shape
        max_dim = link_intersection.shape

        if current_dim >= new_dim:
            raise QRedTeaError(
                f"No link expansion going from {current_dim} to {new_dim}."
            )

        if current_dim == max_dim:
            # Link is at the maximum dimension, user cannot necessarily know,
            # so just return input
            return self, other

        # pylint: disable-next=consider-using-min-builtin
        if max_dim < new_dim:
            # Cannot expand as wished, at least go to what is possible
            new_dim = max_dim
            # raise QRedTeaError("Cannot expand as much as wished.")

        link_expand = self.links[link_self].random_expand(link_intersection, new_dim)

        new_this = self._expand_link_tensor(link_self, link_expand)
        new_other = other._expand_link_tensor(link_other, link_expand)

        if RUN_SANITY_CHECKS:
            # Need to check something here
            newt = deepcopy(new_this)
            newo = deepcopy(new_other)

            newt._remove_duplicates()
            newo._remove_duplicates()

            if len(newt.degeneracy_tensors) != len(new_this.degeneracy_tensors):
                raise QRedTeaAbelianSymError("Created duplicated")

            if len(newo.degeneracy_tensors) != len(new_other.degeneracy_tensors):
                raise QRedTeaAbelianSymError("Created duplicated")

        return new_this, new_other

    def kron(self, other, idxs=None):
        """Kron method. See _AbstractTensor. Not Implemented here"""
        raise NotImplementedError("kron is not implemented for symmetric tensors")

    def split_qr(
        self,
        legs_left,
        legs_right,
        perm_left=None,
        perm_right=None,
        is_q_link_outgoing=True,
        disable_streams=False,
    ):
        """
        Split the tensor via a QR decomposition.

        Parameters
        ----------

        self : instance of :class:`QteaTensor`
            Tensor upon which apply the SVD
        legs_left : list of int
            Legs that will compose the rows of the matrix
        legs_right : list of int
            Legs that will compose the columns of the matrix
        perm_left : list of int, optional
            permutations of legs after the SVD on left tensor
        perm_right : list of int, optional
            permutation of legs after the SVD on right tensor
        disable_streams : boolean, optional
            Can disable streams to avoid nested generation of
            streams.

        Returns
        -------

        tens_left: instance of :class:`QteaTensor`
            unitary tensor after the QR, i.e., Q.
        tens_right: instance of :class:`QteaTensor`
            upper triangular tensor after the QR, i.e., R
        """
        self.sanity_check()

        if self.cs.num_coupling_sectors == 0:
            raise QRedTeaEmptyTensorError(
                "Cannot run QR without coupling sectors!"
                "This might be related to your physics!"
            )

        split_tens, fuse_l, fuse_r = self._split_prepare(legs_left, legs_right)

        nn = len(split_tens.degeneracy_tensors)
        q_tensors = [None] * nn
        r_tensors = [None] * nn

        # Do QR in streams
        streams = [self.stream(disable_streams=disable_streams) for kk in range(nn)]

        split_tens.sanity_check()

        for ii, deg_tens in enumerate(split_tens.degeneracy_tensors):
            with streams[ii]:
                qtens, rtens = deg_tens.split_qr([0], [1])

                q_tensors[ii] = qtens
                r_tensors[ii] = rtens

        self._synchronize_streams(streams)

        q_tensor = self._split_finalize(
            split_tens, 0, legs_left, q_tensors, perm_left, is_q_link_outgoing, fuse_l
        )
        r_tensor = self._split_finalize(
            split_tens, 1, legs_right, r_tensors, perm_right, is_q_link_outgoing, fuse_r
        )

        if RUN_SANITY_CHECKS:
            q_tensor.sanity_check()
            r_tensor.sanity_check()

            if perm_left is None:
                ii = q_tensor.ndim - 1
            else:
                ii = perm_left.index(q_tensor.ndim - 1)

            if perm_right is None:
                jj = 0
            else:
                jj = perm_right.index(0)

            if q_tensor.links[ii] != r_tensor.links[jj]:
                print(
                    "Error information",
                    q_tensor.links[ii].irrep_listing.irreps,
                    r_tensor.links[jj].irrep_listing.irreps,
                    q_tensor.links[ii].irrep_listing.degeneracies,
                    r_tensor.links[jj].irrep_listing.degeneracies,
                )
                raise QRedTeaError("Cannot contract back Q and R.")

        return q_tensor, r_tensor

        # q_tensor = self._split_finalize_left(
        #    split_tens, legs_left, q_tensors, perm_left, is_q_link_outgoing, fuse_l
        # )
        # r_tensor = self._split_finalize_right(
        #    split_tens, legs_right, r_tensors, perm_right, is_q_link_outgoing, fuse_r
        # )

        # return q_tensor, r_tensor

        ## By default summing over irreps, q-link will be outgoing, r-link will
        ## be incoming. Will be modified before return
        # q_outgoing = [split_tens.are_links_outgoing[0], True]
        # r_outgoing = [False, split_tens.are_links_outgoing[1]]

        # q_tensor_rank2 = self._empty_from_links_directions(
        #    split_tens.links, q_outgoing, self.base_tensor_cls
        # )
        # q_tensor_rank2._append_cs(q_tensors, split_tens.cs)

        # r_tensor_rank2 = self._empty_from_links_directions(
        #    split_tens.links, r_outgoing, self.base_tensor_cls
        # )
        # r_tensor_rank2._append_cs(r_tensors, split_tens.cs)

        # olinks = [self.links[ii] for ii in legs_left]
        # are_outgoing = [self._are_links_outgoing[ii] for ii in legs_left]
        # q_tensor = q_tensor_rank2._split_links_with_fuse_rule(
        #    fuse_l, 0, olinks, are_outgoing
        # )

        # olinks = [self.links[ii] for ii in legs_right]
        # are_outgoing = [self._are_links_outgoing[ii] for ii in legs_right]
        # r_tensor = r_tensor_rank2._split_links_with_fuse_rule(
        #    fuse_r, 1, olinks, are_outgoing
        # )

        # if not is_q_link_outgoing:
        #    link_idx = q_tensor.ndim - 1
        #    q_tensor.links = q_tensor._invert_link_selection([link_idx])
        #    q_tensor.are_links_outgoing[link_idx] = False

        #    link_idx = 1
        #    r_tensor.links = r_tensor._invert_link_selection([link_idx])
        #    r_tensor.are_links_outgoing[link_idx] = True

        # if perm_left is not None:
        #    q_tensor.transpose_update(perm_left)

        # if perm_right is not None:
        #    r_tensor.transpose_update(perm_right)

        # if len(q_tensor.degeneracy_tensors) != q_tensor.cs.num_coupling_sectors:
        #    raise QRedTeaAbelianSymError("Mismatch cs and deg-tensor length.")

        # if q_tensor.cs.num_coupling_sectors == 0:
        #    raise QRedTeaEmptyTensorError("Created empty tensors.")

        # if len(r_tensor.degeneracy_tensors) != r_tensor.cs.num_coupling_sectors:
        #    raise QRedTeaAbelianSymError("Mismatch cs and deg-tensor length.")

        # if r_tensor.cs.num_coupling_sectors == 0:
        #    raise QRedTeaEmptyTensorError("Created empty tensors.")

        # return q_tensor, r_tensor

    def split_qrte(
        self,
        tens_right,
        singvals_self,
        operator=None,
        conv_params=None,
        is_q_link_outgoing=True,
    ):
        """Split via a truncated expanded QR."""
        raise NotImplementedError("Truncated Expanded QR for AbelianTensor.")

    def split_rq(
        self,
        legs_left,
        legs_right,
        perm_left=None,
        perm_right=None,
        is_q_link_outgoing=True,
    ):
        """
        Split the tensor via a RQ decomposition. The abstract class defines the RQ
        via a QR and permutation of legs, but we highly recommend overwriting this
        approach with an actual RQ.

        Parameters
        ----------

        self : instance of :class:`_AbstractQteaTensor`
            Tensor upon which apply the RQ
        legs_left : list of int
            Legs that will compose the rows of the matrix (and the R matrix)
        legs_right : list of int
            Legs that will compose the columns of the matrix (and the Q matrix)
        perm_left : list of int | None, optional
            permutations of legs after the QR on left tensor
            Default to `None` (no permutation)
        perm_right : list of int | None, optional
            permutation of legs after the QR on right tensor
            Default to `None` (no permutation)
        is_q_link_outgoing : int, optional
            Direction of link, placeholder for symmetric tensors.
            Default to True.

        Returns
        -------

        tens_left: instance of :class:`_AbstractQteaTensor`
            upper triangular tensor after the RQ, i.e., R
        tens_right: instance of :class:`_AbstractQteaTensor`
            unitary tensor after the RQ, i.e., Q.
        """
        self.sanity_check()

        if self.cs.num_coupling_sectors == 0:
            raise QRedTeaEmptyTensorError(
                "Cannot run RQ without coupling sectors!"
                "This might be related to your physics!"
            )

        split_tens, fuse_l, fuse_r = self._split_prepare(legs_left, legs_right)

        r_tensors = []
        q_tensors = []

        split_tens.sanity_check()

        for deg_tens in split_tens.degeneracy_tensors:
            rtens, qtens = deg_tens.split_rq([0], [1])

            r_tensors.append(rtens)
            q_tensors.append(qtens)

        # Let's us switch to have the flag in the same way based on the left tensor!
        is_r_link_outgoing = not is_q_link_outgoing

        r_tensor = self._split_finalize(
            split_tens, 0, legs_left, r_tensors, perm_left, is_r_link_outgoing, fuse_l
        )
        q_tensor = self._split_finalize(
            split_tens, 1, legs_right, q_tensors, perm_right, is_r_link_outgoing, fuse_r
        )

        if RUN_SANITY_CHECKS:
            r_tensor.sanity_check()
            q_tensor.sanity_check()

            if perm_left is None:
                ii = r_tensor.ndim - 1
            else:
                ii = perm_left.index(r_tensor.ndim - 1)

            if perm_right is None:
                jj = 0
            else:
                jj = perm_right.index(0)

            if r_tensor.links[ii] != q_tensor.links[jj]:
                print(
                    "Error information",
                    r_tensor.links[ii].irrep_listing.irreps,
                    q_tensor.links[jj].irrep_listing.irreps,
                    r_tensor.links[ii].irrep_listing.degeneracies,
                    q_tensor.links[jj].irrep_listing.degeneracies,
                )
                raise QRedTeaError("Cannot contract back R and Q.")

        return r_tensor, q_tensor

    def split_svd(
        self,
        legs_left,
        legs_right,
        perm_left=None,
        perm_right=None,
        contract_singvals="N",
        conv_params=None,
        is_link_outgoing_left=True,
        no_truncation=False,
        disable_streams=False,
    ):
        """
        Perform a truncated Singular Value Decomposition by
        first reshaping the tensor into a legs_left x legs_right
        matrix, and permuting the legs of the ouput tensors if needed.
        If the contract_singvals = ('L', 'R') it takes care of
        renormalizing the output tensors such that the norm of
        the MPS remains 1 even after a truncation.

        Parameters
        ----------
        self : instance of :class:`QteaAbelianTensor`
            Tensor upon which apply the SVD
        legs_left : list of int
            Legs that will compose the rows of the matrix
        legs_right : list of int
            Legs that will compose the columns of the matrix
        perm_left : list of int, optional
            permutations of legs after the SVD on left tensor
        perm_right : list of int, optional
            permutation of legs after the SVD on right tensor
        contract_singvals: string, optional
            How to contract the singular values.
                'N' : no contraction
                'L' : to the left tensor
                'R' : to the right tensor
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use in the procedure. If None is given,
            then use the default convergence parameters of the TN.
            Default to None.
        no_truncation : boolean, optional
            Allow to run without truncation
            Default to `False` (hence truncating by default)
        disable_streams : boolean, optional
            Can disable streams to avoid nested generation of
            streams.

        Returns
        -------
        tens_left: instance of :class:`QteaAbelianTensor`
            left tensor after the SVD
        tens_right: instance of :class:`QteaAbelianTensor`
            right tensor after the SVD
        singvals: :class:`AbelianSymLinkWeights`
            singular values kept after the SVD
        singvals_cut: :class:`AbelianSymLinkWeights`
            singular values cut after the SVD, normalized with the biggest singval
        """
        if len(self.degeneracy_tensors) == 0:
            raise QRedTeaEmptyTensorError("Trying to run SVD on empty tensor.")

        flip = self.degeneracy_tensors[0].get_attr("flip")

        argsort = self.degeneracy_tensors[0].get_attr("argsort")
        split_tens, fuse_l, fuse_r = self._split_prepare(legs_left, legs_right)

        nn = len(split_tens.degeneracy_tensors)
        u_tensors = [None] * nn
        s_tensors = [None] * nn
        v_tensors = [None] * nn
        dim = [None] * nn

        # Do SVD in streams
        streams = [self.stream(disable_streams=disable_streams) for kk in range(nn)]

        for ii, deg_tens in enumerate(split_tens.degeneracy_tensors):
            with streams[ii]:
                u_ii, v_ii, s_ii, _ = deg_tens.split_svd(
                    [0], [1], conv_params=conv_params, no_truncation=True
                )
                u_tensors[ii] = u_ii
                s_tensors[ii] = s_ii
                v_tensors[ii] = v_ii

                dim[ii] = s_ii.shape[0]

        self._synchronize_streams(streams)
        dim = int(np.sum(np.array(dim)))

        lambdas_all, mapping = self.degeneracy_tensors[0].concatenate_vectors(
            s_tensors, s_tensors[0].dtype, dim=dim
        )

        inds = argsort(lambdas_all)
        inds = flip(inds, (0,))
        if hasattr(self.degeneracy_tensors[0], "gather"):
            # tensorflow problem as usual with [] syntax
            lambdas_all = self.degeneracy_tensors[0].gather(lambdas_all, inds)
        else:
            lambdas_all = lambdas_all[inds]

        # pylint: disable-next=no-else-raise
        if no_truncation:
            # This flag was mainly to be able to get SVDs without truncation
            # when calling from here, not into here, but anyway ...
            ncut = dim
        else:
            ncut, s_kept, s_cut = self.degeneracy_tensors[0]._truncate_singvals(
                lambdas_all, conv_params=conv_params
            )

        mask_device = self.degeneracy_tensors[0].mask_to_device(bmaskf(dim))

        if isinstance(mask_device, np.ndarray):
            mask_device[inds[:ncut]] = True
        elif self.linear_algebra_library == "tensorflow":
            convert_to_tensor = self.degeneracy_tensors[0].get_attr("convert_to_tensor")
            mask_lst = [False] * len(inds)
            for idx in inds[:ncut]:
                mask_lst[idx] = True
            mask_new = convert_to_tensor(mask_lst)
            mask_device = self.degeneracy_tensors[0].mask_to_device(mask_new)
        elif self.linear_algebra_library == "jax":
            mask_device = mask_device.at[inds[:ncut]].set(True)
        else:
            mask_device[inds[:ncut]] = True
        mask_host = self.degeneracy_tensors[0].mask_to_host(mask_device)

        s_tensors_kept = []
        deg_kept = []
        deg_cut = []
        s_tensors_cut = []

        degs_fuse_l = fuse_l["link"].irrep_listing.degeneracies.copy()
        degs_fuse_r = fuse_r["link"].irrep_listing.degeneracies.copy()

        for ii, s_tensors_ii in enumerate(s_tensors):
            k1, k2 = mapping[ii]
            sub_mask_host = mask_host[k1:k2]
            sub_mask_device = mask_device[k1:k2]
            s_kept = s_tensors_ii[sub_mask_device]
            deg = isum(sub_mask_host)
            deg_kept.append(deg)

            if deg > 0:
                s_tensors_kept.append(s_kept)
            else:
                # For finalizing link, the list must respect the original
                # coupling sector order of `split_tens`. We need one element
                # even if it is `None`
                s_tensors_kept.append(None)

            sub_mask_host = ilogical_not(sub_mask_host)
            s_cut = s_tensors_ii[sub_mask_host]
            s_tensors_cut.append(s_cut)
            deg_cut.append(isum(sub_mask_host))

            if deg == 0:
                u_tensors[ii] = None
                v_tensors[ii] = None

            elif isum(sub_mask_host) > 0:
                # Update U and V
                new_u = self.base_tensor_cls.from_elem_array(
                    u_tensors[ii].elem[:, :deg]
                )
                new_v = self.base_tensor_cls.from_elem_array(
                    v_tensors[ii].elem[:deg, :]
                )

                u_tensors[ii] = new_u
                v_tensors[ii] = new_v
            # else:
            # Keeping all, no update of degeneracy dimension necessary

            if (deg > 0) and (contract_singvals.upper() == "L"):
                u_tensors[ii].scale_link_update(s_kept, 1)
            elif (deg > 0) and (contract_singvals.upper() == "R"):
                v_tensors[ii].scale_link_update(s_kept, 0)
            elif (deg > 0) and (contract_singvals.upper() != "N"):
                raise ValueError(
                    f"Contract_singvals option {contract_singvals} is not "
                    + "implemented. Choose between right (R), left (L) or None (N)."
                )

        # Update complete links
        irrep_list_l = IrrepListing.from_irreps(
            self.sym,
            fuse_l["link"].irrep_listing.irreps,
            degs_fuse_l,
            are_sorted=True,
            remove_trivial=False,
            are_unique=True,
        )
        irrep_list_r = IrrepListing.from_irreps(
            self.sym,
            fuse_r["link"].irrep_listing.irreps,
            degs_fuse_r,
            are_sorted=True,
            remove_trivial=False,
            are_unique=True,
        )

        fuse_l["link"] = AbelianSymLink(self.sym, irrep_list_l)
        fuse_r["link"] = AbelianSymLink(self.sym, irrep_list_r)

        if ncut == dim:
            deg_kept = None

        u_tensor = self._split_finalize(
            split_tens,
            0,
            legs_left,
            u_tensors,
            perm_left,
            is_link_outgoing_left,
            fuse_l,
            new_deg=deg_kept,
        )

        v_tensor = self._split_finalize(
            split_tens,
            1,
            legs_right,
            v_tensors,
            perm_right,
            is_link_outgoing_left,
            fuse_r,
            new_deg=deg_kept,
        )

        idx_r = 0 if perm_right is None else perm_right.index(0)
        weights = self._split_finalize_weights(
            split_tens,
            s_tensors_kept,
            v_tensor.links[idx_r],
            is_link_outgoing_left,
        )
        weights_cut = self._split_finalize_weights(
            split_tens,
            s_tensors_cut,
            v_tensor.links[idx_r],
            is_link_outgoing_left,
            allow_empty=True,
        )

        if RUN_SANITY_CHECKS:
            idx_r = 0 if perm_right is None else perm_right.index(0)
            idx_l = (
                u_tensor.ndim - 1
                if perm_left is None
                else perm_left.index(u_tensor.ndim - 1)
            )

            u_tensor.sanity_check()
            v_tensor.sanity_check()
            weights.sanity_check()

            if perm_left is None:
                ii = u_tensor.ndim - 1
            else:
                ii = perm_left.index(u_tensor.ndim - 1)

            if perm_right is None:
                jj = 0
            else:
                jj = perm_right.index(0)

            if u_tensor.links[ii] != v_tensor.links[jj]:
                print("Permutations, indices", ii, jj, perm_left, perm_right)
                print("Shapes", u_tensor.shape, v_tensor.shape)
                print(
                    "Error information",
                    u_tensor.links[ii].irrep_listing.irreps,
                    v_tensor.links[jj].irrep_listing.irreps,
                    u_tensor.links[ii].irrep_listing.degeneracies,
                    v_tensor.links[jj].irrep_listing.degeneracies,
                )
                raise QRedTeaError("Cannot contract back U and V.")

            v_tensor.scale_link(weights, idx_r)
            u_tensor.scale_link(weights, idx_l)

        return u_tensor, v_tensor, weights, weights_cut

    def stack_link(self, other, link):
        """
        Stack two tensors along a given link.

        **Arguments**

        other : instance of :class:`QteaAbelianTensor`
            Links must match `self` up to the specified link.

        link : integer
            Stack along this link.

        **Returns**

        new_this : instance of :class:QteaAbelianTensor`
        """
        if self.ndim != other.ndim:
            raise QRedTeaRankError("Different number of links.")

        for ii in range(self.ndim):
            if self._are_links_outgoing[ii] != other.are_links_outgoing[ii]:
                raise QRedTeaLinkError(f"Direction link {ii} not matching.")

            if (self.links[ii] != other.links[ii]) and (ii != link):
                raise QRedTeaLinkError(f"Link {ii} not matching.")

        raise NotImplementedError("A bit tricky with irreps and cs.")

    def stack_first_and_last_link(self, other):
        """
        Stack first and last link of tensor targeting MPS addition (not implemented).
        """
        raise NotImplementedError("A bit tricky with irreps and cs.")

    def tensordot(self, other, contr_idx, disable_streams=False):
        """Tensor contraction of two tensors along the given indices."""
        # contraction links
        c_links_a = contr_idx[0]
        c_links_b = contr_idx[1]

        c_out_a = [self._are_links_outgoing[ii] for ii in c_links_a]
        c_out_b = [other.are_links_outgoing[ii] for ii in c_links_b]

        if len(c_links_a) != len(c_links_b):
            raise QRedTeaRankError("Mismatch number of links.")

        for ii, idx in enumerate(c_links_a):
            jj = c_links_b[ii]

            # Can only contract incoming with outgoing or vice versa
            if self._are_links_outgoing[idx] == other.are_links_outgoing[jj]:
                msg = "Mismatch link directions: ["
                msg += ", ".join(map(str, c_out_a)) + "] vs ["
                msg += ", ".join(map(str, c_out_b)) + "]"
                raise QRedTeaLinkError(msg)

            if self.links[idx] != other.links[jj]:
                remove_trivial_a = self.links[idx].remove_trivial()
                remove_trivial_b = other.links[jj].remove_trivial()

                print(
                    "Error information",
                    f"link index self {idx}",
                    f"link index other {jj}",
                    self.links[idx].irrep_listing.irreps,
                    other.links[jj].irrep_listing.irreps,
                    self.links[idx].irrep_listing.degeneracies,
                    other.links[jj].irrep_listing.degeneracies,
                    "\nNon-trivial equal",
                    remove_trivial_a == remove_trivial_b,
                )
                raise QRedTeaLinkError("Link mismatch.")

        # remaining links
        r_links_a = self._invert_link_selection(c_links_a)
        r_links_b = other._invert_link_selection(c_links_b)

        links_ab = [self.links[ii] for ii in r_links_a]
        links_ab += [other.links[ii] for ii in r_links_b]

        out_ab = [self._are_links_outgoing[ii] for ii in r_links_a]
        out_ab += [other.are_links_outgoing[ii] for ii in r_links_b]

        # Can be extended to check what is hashed already
        if self.cs.num_coupling_sectors < other.cs.num_coupling_sectors:
            collect_matches = self._matches_tensordot_hash_self(other, contr_idx)
        else:
            collect_matches = self._matches_tensordot_hash_other(other, contr_idx)

        nn = len(collect_matches)
        mm_a = len(r_links_a)
        mm = mm_a + len(r_links_b)
        cs = indarray((nn, mm))
        degeneracy_tensors = []

        # Contract tensor pairs with streams
        streams = [
            self.stream(disable_streams=disable_streams)
            for kk in range(len(collect_matches))
        ]
        for kk, pair in enumerate(collect_matches):
            with streams[kk]:
                ii, jj = pair

                cs[kk, :mm_a] = self.cs.denormalized_sectors[ii, r_links_a]
                cs[kk, mm_a:] = other.cs.denormalized_sectors[jj, r_links_b]

                tensor_kk = self.degeneracy_tensors[ii].tensordot(
                    other.degeneracy_tensors[jj],
                    contr_idx,
                )

            degeneracy_tensors.append(tensor_kk)

        self._synchronize_streams(streams)

        if len(links_ab) == 0:
            ctensor = QteaAbelianTensor(
                [],
                are_links_outgoing=[],
                device=self.device,
                dtype=self.dtype,
                base_tensor_cls=self.base_tensor_cls,
            )

            if len(degeneracy_tensors) > 0:
                elem = degeneracy_tensors[0]
                for subelem in degeneracy_tensors[1:]:
                    elem.add_update(subelem)

                cs = izeros([1, 0])

                ctensor._append_cs([elem], cs)

        else:
            ctensor = self._empty_from_links_directions(
                links_ab, out_ab, self.base_tensor_cls
            )
            ctensor._append_cs(degeneracy_tensors, cs)
            ctensor._remove_duplicates()

        if len(ctensor.degeneracy_tensors) != ctensor.cs.num_coupling_sectors:
            raise QRedTeaAbelianSymError("Mismatch cs and deg-tensor length.")

        return ctensor

    def stream(self, disable_streams=False):
        """
        Get the instance of a context which can be used to parallelize.
        Symmetric tensors always go via the base tensor class.

        Parameters
        ----------

        disable_streams : bool, optional
            Allows to disable streams to avoid nested creation of
            streams. Globally, streams should be disabled via the
            `set_streams_*` function of the corresponding
            base tensor module.
            Default to False.

        Returns
        -------

        Context manager, e.g.,
        :class:`Stream` if running on GPU and enabled or
        :class:`nullcontext(AbstractContextManager)` otherwise.

        """
        if len(self.degeneracy_tensors) == 0:
            raise QRedTeaEmptyTensorError("Cannot generate stream from empty tensor")

        return self.degeneracy_tensors[0].stream(disable_streams=disable_streams)

    # --------------------------------------------------------------------------
    #                       Gradient descent: backwards propagation
    # --------------------------------------------------------------------------
    # pylint: disable=missing-function-docstring

    @staticmethod
    def get_optimizer(*args, **kwargs):
        raise QRedTeaError("Function not implemented in this class")

    def backward(self, **kwargs):
        raise QRedTeaError("Function not implemented in this class")

    # pylint: enable=missing-function-docstring
    # --------------------------------------------------------------------------
    #                        Internal methods
    # --------------------------------------------------------------------------
    #
    # inherit _invert_link_selection

    # --------------------------------------------------------------------------
    #                                MISC
    # --------------------------------------------------------------------------

    def get_of(self, variable):
        """Get the whole array of a tensor to the host as tensor."""
        if len(self.degeneracy_tensors) > 0:
            return self.degeneracy_tensors[0].get_of(variable)

        raise QRedTeaEmptyTensorError("Method requires at least on degeneracy tensor.")

    def is_gpu_available(self):
        """Return if GPU is available as device (based on the base_tensor_cls."""
        return self.base_tensor_cls.is_gpu_available()

    def get_attr(self, *args):
        """Collect attribute via underlying degeneracy tensor."""
        if len(self.degeneracy_tensors) == 0:
            raise QRedTeaEmptyTensorError(
                "Method requires at least on degeneracy tensor."
            )
        return self.degeneracy_tensors[0].get_attr(*args)

    # --------------------------------------------------------------------------
    #             Internal methods (not required by abstract class)
    # --------------------------------------------------------------------------

    def _append_cs(self, degeneracy_tensors, cs):
        """Append new CS and degeneracy tensor to existing tensor (inplace update)."""
        if isinstance(cs, CouplingSectors):
            # Right now, we want to be able to either append CS instance
            # or denormalized sectors as np.ndarray
            cs = cs.denormalized_sectors

        if self.cs.num_coupling_sectors == 0:
            # Empty tensor so far
            self.cs = CouplingSectors(cs)
            self.degeneracy_tensors = degeneracy_tensors
            return self

        # Tensors has already coupling sectors
        num_cs_a = self.cs.num_coupling_sectors
        num_cs_b = cs.shape[0]

        num_cs = num_cs_a + num_cs_b

        cs = indarray((num_cs, self.ndim))
        cs[:num_cs_a, :] = self.cs.denormalized_sectors
        cs[num_cs_a:, :] = cs

        self.cs = CouplingSectors(cs)
        self.degeneracy_tensors += degeneracy_tensors

        return self

    def _assert_cs_active(self, fix_instead_of_error=False):
        for ii, link in enumerate(self.links):
            not_visited = bmaskt(len(link.irrep_listing))

            for _, cs_jj in self.cs.iter_sectors():
                not_visited[cs_jj[ii]] = False

            if iany(not_visited) and fix_instead_of_error:
                mask = ilogical_not(not_visited)
                irreps = link.irrep_listing.irreps[mask, :]
                deg = link.irrep_listing.degeneracies[mask]
                irrep_list = IrrepListing.from_irreps(
                    link.sym, irreps, deg, are_sorted=True, are_unique=True
                )
                new_link = AbelianSymLink(self.sym, irrep_list)
                self._link_update(ii, new_link)
            elif iany(not_visited):
                raise QRedTeaLinkError(f"CS in link {ii} not needed.")

    def _compress(self, tol=0.0):
        """Compress away degeneracy tensors below the tolerance. Links are not compressed."""
        nn = len(self.degeneracy_tensors)
        mask_keep = bmaskt(nn)

        new_deg_tensors = []
        for ii, tensor in enumerate(self.degeneracy_tensors):
            mask_keep[ii] = tensor.norm() > tol
            if mask_keep[ii]:
                new_deg_tensors.append(tensor)

        cs = self.cs.denormalized_sectors[mask_keep, :]
        self.cs = CouplingSectors(cs, sorted_for=self.cs.sorted_for)
        self.degeneracy_tensors = new_deg_tensors

    @classmethod
    def _empty_from_links_directions(cls, links, are_links_outgoing, base_tensor_cls):
        """Create empty tensor without coupling sectors just from links and directions."""
        obj = cls(
            links,
            are_links_outgoing=are_links_outgoing,
            base_tensor_cls=base_tensor_cls,
        )

        obj.cs = CouplingSectors(indarray((0, obj.ndim)))
        # obj.are_links_outgoing = are_links_outgoing
        obj.degeneracy_tensors = []

        return obj

    def _expand_link_tensor(self, link_idx, link_expanded):
        """Expand the tensor along one link with the given new link."""

        self.sanity_check()

        elinks = self.links[:link_idx] + [link_expanded] + self.links[link_idx + 1 :]

        etens = QteaAbelianTensor(
            elinks,
            ctrl="R",
            are_links_outgoing=self._are_links_outgoing,
            device=self.device,
            dtype=self.dtype,
            base_tensor_cls=self.base_tensor_cls,
        )

        # Updated links
        ulink = self.links[link_idx].stack_link(elinks[link_idx])

        # Force them into the current tensors (coupling sectors have to be updated
        # as there might be new irreps)
        etens._link_update(link_idx, ulink)

        # Generate hashes on all links
        etens.cs.generate_hashes(list(range(etens.ndim)))

        new_this = QteaAbelianTensor(
            self.links.copy(),
            are_links_outgoing=self._are_links_outgoing.copy(),
            device=self.device,
            dtype=self.dtype,
            base_tensor_cls=self.base_tensor_cls,
        )
        new_this._link_update(link_idx, ulink)

        dummy = []
        cs = []
        deg_tensors = []
        for ii, elem in self.cs.iter_sectors():
            jj = elem[link_idx]
            irrep = self.links[link_idx].irrep_listing.irreps[jj, :]
            kk = ulink.irrep_listing.index(irrep)

            new_kk = kk

            e_elem = []
            for kk in range(self.ndim):
                jj = elem[kk]
                irrep = self.links[kk].irrep_listing.irreps[jj, :]
                idx = etens.links[kk].irrep_listing.index(irrep)
                e_elem.append(idx)

            elem[link_idx] = new_kk
            cs.append(elem)
            dummy.append(tuple(elem))

            idx = etens.cs[e_elem]  # THIS ELEM IS WRONG - DIFFERENT CS
            if idx[0] is None:
                deg_tensors.append(self.degeneracy_tensors[ii])
            elif len(idx) > 1:
                raise QRedTeaAbelianSymError("Full hash should only lead to one index.")
            else:
                tens = self.degeneracy_tensors[ii]
                tens_e = etens.degeneracy_tensors[idx[0]]
                tens = tens.stack_link(tens_e, link_idx)
                deg_tensors.append(tens)

        for ii, elem in etens.cs.iter_tracker_false():
            cs.append(elem)
            dummy.append(tuple(elem))
            deg_tensors.append(etens.degeneracy_tensors[ii])

        cs = iarray(cs)
        new_this._append_cs(deg_tensors, cs)

        new_this.sanity_check()

        return new_this

    @classmethod
    def _from_base_tensor(
        cls, elem, irreps_inds, irreps_strides, link, base_tensor_cls
    ):
        """
        Generate symmetric tensor from base tensor and irreps.

        **Arguments**

        elem : instance of base tensor

        irreps_inds : integer array
            How to sort rows/cols according to irreps in generators

        irreps_strides : dict
             Containing ...

        link : instance of :class:`AbelianSymLink`
            Full link with all irreps according to generator.

        base_tensor_cls : `_AbstractQteaBaseTensor`

        **Details**

        Returns rank-4 with [incoming, incoming, outgoing, outgoing], where the
        links are [dummy, ket, bra, delta] and delta carries the difference between
        the rows/ket and the columns/bra of the operator.
        """
        # Permute into block-diagonal shape
        elem.permute_rows_cols_update(irreps_inds)

        num_max_cs = len(irreps_strides) ** 2

        degeneracy_tensors = []
        cs = izeros((num_max_cs, 4))
        ii = 0
        irrep_d = None

        # Loop over rows and columns
        for key_j in irreps_strides.keys():
            # Difference key_j and irrep_j is just tuple vs np.ndarray
            idx_j, j1, j2 = irreps_strides[key_j]
            irrep_j = link.irrep_listing.irreps[idx_j, :]

            for key_k in irreps_strides.keys():
                idx_k, k1, k2 = irreps_strides[key_k]
                irrep_k = link.irrep_listing.irreps[idx_k, :]
                deg_tens = elem.get_submatrix((j1, j2), (k1, k2))

                if deg_tens.elementwise_abs_smaller_than(1e-14):
                    continue

                diff = link.sym.decouple_irreps(irrep_j, irrep_k)
                if irrep_d is None:
                    irrep_d = diff
                elif not IrrepListing.is_equal_irrep(irrep_d, diff):
                    # Maybe too restrictive, but different deltas would
                    # allow to couple for example sector 0 <--> 1 and
                    # in the same operators 0 <--> 2, which should lead
                    # to some problems.
                    raise QRedTeaAbelianSymError("Operator has different deltas.")

                # Symmetric tensor will have four links
                shape = [1] + list(deg_tens.shape) + [1]
                deg_tens.reshape_update(shape)

                degeneracy_tensors.append(deg_tens)
                cs[ii, 1:3] = [idx_j, idx_k]
                ii += 1

        if ii == 0:
            # Not a single degeneracy tensors is non-zero
            # (add first or trivial irreps)
            raise NotImplementedError("Operators with all zeros.")

        dummy = AbelianSymLink.create_dummy(link.sym)
        links = [dummy, link, link, deepcopy(link)]

        irrep_d = irrep_d.reshape([1, irrep_d.shape[0]])
        irrep_listing = IrrepListing.from_irreps(link.sym, irrep_d, iones([1]))
        idx_d = links[-1].irrep_listing.index(irrep_d)
        if idx_d is None:
            links[-1] = links[-1].invert()

        try:
            links[-1].restrict_irreps(irrep_listing)
        except QRedTeaAbelianSymError:
            # This can happen if the the operator's horizontal links
            # carries only the trivial irrep, but the local Hilbert
            # space does not contain the trivial irreps. Then, restricting
            # the irreps will lead to an empty link and this error. Re-run
            # restricting the dummy link to make sure the operator's horizontal
            # links are actually dummy links.
            try:
                links[-1] = deepcopy(dummy)
                links[-1].restrict_irreps(irrep_listing)
            except QRedTeaAbelianSymError:
                # Still can happen for non-zero irreps where the irreps
                # is no valid basis state, e.g., generators [0, 1, 1] and
                # [1, 2, 0] with and irreps [1, 1]. I fear we have to construct
                # the link by hand ... in theory, the irreps can have arbitrary
                # signs now, fix the first irreps to be non-negative.
                link_d = AbelianSymLink(link.sym, irrep_listing)

                if irrep_d[0, 0] < 0:
                    link_d = link_d.invert()
                    irrep_df = link_d.irrep_listing.irreps[0, :]
                    irrep_df = irrep_df.reshape([1, irrep_df.shape[0]])

                    irrep_listing = IrrepListing.from_irreps(
                        link.sym, irrep_df, iones([1])
                    )
                    link_d = AbelianSymLink(link.sym, irrep_listing)
                    link_d = link_d.invert()

                links[-1] = link_d

        cs = cs[:ii, :]
        cs[:, 0] = links[0].irrep_listing.index(link.sym.identical_irrep)
        cs[:, 3] = links[-1].irrep_listing.index(irrep_d)

        obj = cls._empty_from_links_directions(
            links, [False, False, True, True], base_tensor_cls
        )
        obj._append_cs(degeneracy_tensors, cs)

        return obj

    def _from_vector(self, vec, mapping):
        """Use mapping to generate a tensor similar to `self` with entries of vector."""

        if RUN_SANITY_CHECKS:
            self.sanity_check()

        tens = self._empty_from_links_directions(
            self.links, self._are_links_outgoing, self.base_tensor_cls
        )

        cs = self.cs
        deg_tensors = []
        for _, cs_ii in self.cs.iter_sectors():
            key = tuple(cs_ii)

            k1, k2, shape = mapping[key]
            elem = vec[k1:k2].reshape(shape)
            deg_tens = self.degeneracy_tensors[0].from_elem_array(elem)
            deg_tensors.append(deg_tens)

        tens._append_cs(deg_tensors, cs)

        if RUN_SANITY_CHECKS:
            tens.sanity_check()

        return tens

    def _fuse_links_for_split(self, span_a):
        """
        Fuse links such that tensor becomes rank-2

        **Arguments**

        span_a : int
            Number of links in first bipartition.

        **Details**

        Targets decompositions; therefore links have already
        been permuted and bipartition is the only option.
        """

        span_b = self.ndim - span_a

        if span_a > 1:
            link_a, fuse_rule_forward_a = self._fuse_prepare(0, span_a - 1)

            # Generate the new link with all possible irreps
            # link_a = AbelianSymLink.from_link_list(
            #    self.links[:span_a], self._are_links_outgoing[:span_a]
            # )

            # Have to merge actual irreps in coupling sectors
            # irrep, degs = self.links[0].select_irreps(
            #    self.cs.get_col(0), do_return_deg=True
            # )
            # degs = [degs]

            # if self._are_links_outgoing[0]:
            #    irrep = self.sym.invert_irrep(irrep)

            # for ii, link in enumerate(self.links[:span_a]):
            #    if ii == 0:
            #        # First is done before loop already
            #        continue

            #    irrep_b, degs_b = link.select_irreps(
            #        self.cs.get_col(ii), do_return_deg=True
            #    )
            #    degs.append(degs_b)

            #    if self._are_links_outgoing[ii]:
            #        irrep_b = self.sym.invert_irrep(irrep_b)

            #    for jj in range(irrep.shape[0]):
            #        # Cannot couple (n x ..) with (n x ..) for any n > 1
            #        # but can be implemented
            #        irrep[jj, :] = self.sym.couple_irreps(irrep[jj, :], irrep_b[jj, :])

            ## deg_a as second return value was unused, same as degs?
            ## See span_b > 1 case ...
            # cs_a, _, inds_a = link_a.generate_cs(irrep)

            # fuse_rule_forward_a = self.links[0].generate_fuse_rule(
            #    cs_a, degs, inds_a, self.cs.denormalized_sectors[:, :span_a]
            # )

        elif self._are_links_outgoing[0]:
            # Need to invert
            link_a = self.links[0].invert()
            fuse_rule_forward_a = {"deg": {}}
            for kk, jj in enumerate(self.cs.denormalized_sectors[:, 0]):
                irrep = self.links[0].irrep_listing.irreps[jj, :]
                irrep = self.sym.invert_irrep(irrep)
                ii = link_a.irrep_listing.index(irrep, require_match=True)
                deg = link_a.irrep_listing.degeneracies[ii]
                fuse_rule_forward_a[tuple((jj,))] = (ii, 0, deg, [deg])
                fuse_rule_forward_a["deg"][ii] = deg
        else:
            link_a = self.links[0]
            fuse_rule_forward_a = {"deg": {}}
            for ii in self.cs.denormalized_sectors[:, 0]:
                deg = link_a.irrep_listing.degeneracies[ii]
                fuse_rule_forward_a[tuple((ii,))] = (ii, 0, deg, [deg])
                fuse_rule_forward_a["deg"][ii] = deg

            # num_cs_a = len(set(self.cs.denormalized_sectors[:, 0]))
            # fuse_rule_a = None

        if span_b > 1:
            link_b, fuse_rule_forward_b = self._fuse_prepare(
                span_a, self.ndim - 1, is_outgoing=False
            )

            # Generate the new link with all possible irreps
            # link_b = AbelianSymLink.from_link_list(
            #    self.links[span_a:], self._are_links_outgoing[span_a:]
            # )

            # Have to merge actual irreps in coupling sectors
            # ii = span_a
            # irrep = self.links[ii].select_irreps(self.cs.get_col(ii))

            # if self._are_links_outgoing[ii]:
            #    irrep = self.sym.invert_irrep(irrep)

            # for _ in range(span_b - 1):
            #    ii += 1

            #    irrep_b = self.links[ii].select_irreps(self.cs.get_col(ii))

            #    if self._are_links_outgoing[ii]:
            #        irrep_b = self.sym.invert_irrep(irrep_b)

            #    irrep = self.sym.couple_irreps(irrep, irrep_b)

            # cs_b, deg_b, inds_b = link_b.generate_cs(irrep)

            # Do we need degs as in span_a loop???
            # fuse_rule_forward_b = self.links[0].generate_fuse_rule(
            #    cs_b, deg_b, inds_b, self.cs_denormalized_sectors[:, span_a:]
            # )

        elif self._are_links_outgoing[-1]:
            link_b = self.links[-1]
            fuse_rule_forward_b = {"deg": {}}
            for kk, ii in enumerate(self.cs.denormalized_sectors[:, -1]):
                deg = link_b.irrep_listing.degeneracies[ii]
                fuse_rule_forward_b[tuple((ii,))] = (ii, 0, deg, [deg])
                fuse_rule_forward_b["deg"][ii] = deg

                if deg != self.degeneracy_tensors[kk].shape[-1]:
                    print("Deg", deg, self.degeneracy_tensors[kk].shape)
                    raise QRedTeaAbelianSymError("Degeneracy dimension mismatch.")
        else:
            link_b = self.links[-1].invert()
            fuse_rule_forward_b = {"deg": {}}
            for kk, jj in enumerate(self.cs.denormalized_sectors[:, -1]):
                irrep = self.links[-1].irrep_listing.irreps[jj, :]
                irrep = self.sym.invert_irrep(irrep)
                ii = link_b.irrep_listing.index(irrep, require_match=True)
                deg = link_b.irrep_listing.degeneracies[ii]
                fuse_rule_forward_b[tuple((jj,))] = (ii, 0, deg, [deg])
                fuse_rule_forward_b["deg"][ii] = deg

                if deg != self.degeneracy_tensors[kk].shape[-1]:
                    print("Deg", deg, self.degeneracy_tensors[kk].shape)
                    raise QRedTeaAbelianSymError("Degeneracy dimension mismatch.")

        tracker = {}
        deg_tensors = []
        idx = -1
        cs = indarray((self.cs.num_coupling_sectors, 2))

        for ii in range(self.cs.num_coupling_sectors):
            key_a = tuple(self.cs.denormalized_sectors[ii, :span_a])
            key_b = tuple(self.cs.denormalized_sectors[ii, span_a:])

            key_ab = (
                fuse_rule_forward_a[key_a][0],
                fuse_rule_forward_b[key_b][0],
            )

            if key_ab not in tracker:
                idx += 1

                cs[idx, :] = key_ab
                tracker[key_ab] = idx
                d_a = fuse_rule_forward_a["deg"][key_ab[0]]
                d_b = fuse_rule_forward_b["deg"][key_ab[1]]

                deg_tensor = self.base_tensor_cls(
                    [d_a, d_b], ctrl="Z", device=self.device, dtype=self.dtype
                )
                deg_tensors.append(deg_tensor)

                jj = idx
            else:
                d_a = fuse_rule_forward_a["deg"][key_ab[0]]
                d_b = fuse_rule_forward_b["deg"][key_ab[1]]
                jj = tracker[key_ab]

            j1 = fuse_rule_forward_a[key_a][1]
            j2 = fuse_rule_forward_a[key_a][2]
            k1 = fuse_rule_forward_b[key_b][1]
            k2 = fuse_rule_forward_b[key_b][2]

            deg_tensors[jj].set_submatrix(
                (j1, j2), (k1, k2), self.degeneracy_tensors[ii]
            )

        new_link_a, new_link_b = link_a.helper_split(link_b)
        fuse_rule_forward_a["link"] = new_link_a
        fuse_rule_forward_b["link"] = new_link_b

        links_fused = [link_a, link_b]
        outgoing_fused = [False, True]
        cs = cs[: idx + 1, :]
        tensor_fused = self._empty_from_links_directions(
            links_fused, outgoing_fused, self.base_tensor_cls
        )
        tensor_fused._append_cs(deg_tensors, cs)

        return tensor_fused, fuse_rule_forward_a, fuse_rule_forward_b

    def _fuse_prepare(self, fuse_low, fuse_high, is_outgoing=True):
        """Prepare a fuse by generating the new link."""
        # Generate the new link with all possible irreps
        # link_a = AbelianSymLink.from_link_list(
        #    self.links[fuse_low : fuse_high + 1],
        #    self._are_links_outgoing[fuse_low : fuse_high + 1],
        # )

        if RUN_SANITY_CHECKS:
            num_cs = self.cs.num_coupling_sectors

        # Have to merge actual irreps in coupling sectors
        ii = fuse_low
        irrep, degs = self.links[ii].select_irreps(
            self.cs.get_col(ii), do_return_deg=True
        )
        degs = [degs]

        if self._are_links_outgoing[ii]:
            irrep = self.sym.invert_irrep(irrep)

        for ii in range(fuse_low + 1, fuse_high + 1):
            link = self.links[ii]

            irrep_b, degs_b = link.select_irreps(
                self.cs.get_col(ii), do_return_deg=True
            )
            degs.append(degs_b)

            if self._are_links_outgoing[ii]:
                irrep_b = self.sym.invert_irrep(irrep_b)

            for jj in range(irrep.shape[0]):
                # Cannot couple (n x ..) with (n x ..) for any n > 1
                # but can be implemented
                irrep[jj, :] = self.sym.couple_irreps(irrep[jj, :], irrep_b[jj, :])

        if not is_outgoing:
            irrep = self.sym.invert_irrep(irrep)

        # Accumulate degeneracies
        cdegs = degs[0].copy()
        for elem in degs[1:]:
            cdegs *= elem
        sym = self.links[fuse_low].sym
        irrep_listing = IrrepListing.from_irreps(sym, irrep, cdegs)
        link_a = AbelianSymLink(sym, irrep_listing)

        # deg_a as second return value was unused, same as degs?
        # See span_b > 1 case ...
        cs_a, _, inds_a = link_a.generate_cs(irrep)
        fuse_rule_forward = self.links[0].generate_fuse_rule(
            cs_a,
            degs,
            inds_a,
            self.cs.denormalized_sectors[:, fuse_low : fuse_high + 1],
        )

        if RUN_SANITY_CHECKS:
            if num_cs != cs_a.shape[0]:
                raise QRedTeaAbelianSymError("Dimension mismatch coupling sectors.")

        # See generate_fuse_rule to see where degeneracy is off
        alternative_irrep = IrrepListing.from_irreps(
            sym, link_a.irrep_listing.irreps, fuse_rule_forward["deg_list"]
        )
        alternative_link = AbelianSymLink(sym, alternative_irrep)

        return alternative_link, fuse_rule_forward

    def _is_valid_cs(self, cs):
        """Check if a given cs is a valid combination of irrep."""
        if self.ndim == 0:
            # No links means scalar, always valid
            return True

        irrep = self.links[0].select_irreps(cs[0])
        identical = self.links[0].sym.identical_irrep
        if self.ndim == 1:
            # One link, only identical irrep can be valid
            return self.links[0].irrep_listing.is_equal_irrep(irrep, identical)

        if self._are_links_outgoing[0]:
            irrep = self.links[0].sym.invert_irrep(irrep)

        for ii, link in enumerate(self.links[1:]):
            irrep_b = link.select_irreps(cs[ii + 1])

            if self._are_links_outgoing[ii + 1]:
                irrep_b = link.sym.invert_irrep(irrep_b)

            irrep = link.sym.couple_irreps(irrep, irrep_b)

        return self.links[0].irrep_listing.is_equal_irrep(irrep, identical)

    def _link_update(self, link_idx, link):
        """Update the link at index `idx` (re-calculate CS)."""
        self._set_link(link, link_idx)
        return

        # Old implementation ... does it do the same?
        # old_link = self.links[link_idx]
        # self.links[link_idx] = link

        # for ii, elem in self.cs.iter_sectors():
        #    jj = elem[link_idx]
        #    irrep = old_link.irrep_listing.irreps[jj, :]
        #    kk = link.irrep_listing.index(irrep)

        #    self.cs.denormalized_sectors[ii, link_idx] = kk

        # return self

    def _mapping_to_vec(self):
        """Generate dict containing the mapping from tensor to vec."""
        mapping = {}

        k2 = 0
        for ii, cs_ii in self.cs.iter_sectors():
            tens = self.degeneracy_tensors[ii]
            k1 = k2
            k2 += iproduct(tens.shape)

            mapping[tuple(cs_ii)] = (k1, k2, tens.shape)

        mapping["dim"] = k2

        return mapping

    def _matches_tensordot_hash_self(self, other, contr_idx):
        """Collect matches for tensordot hashing cs of self."""
        # contraction links
        c_links_a = contr_idx[0]
        c_links_b = contr_idx[1]

        self.cs.generate_hashes(c_links_a)

        collect_matches = []
        for ii, elem in other.cs.iter_sectors():
            key = elem[c_links_b]
            idx_list = self.cs[key]

            if idx_list[0] is None:
                continue

            for jj in idx_list:
                collect_matches.append((jj, ii))

        return collect_matches

    def _matches_tensordot_hash_other(self, other, contr_idx):
        """Collect matches for tensordot hashing cs of other."""
        # contraction links
        c_links_a = contr_idx[0]
        c_links_b = contr_idx[1]

        other.cs.generate_hashes(c_links_b)

        collect_matches = []
        for ii, elem in self.cs.iter_sectors():
            key = elem[c_links_a]

            idx_list = other.cs[key]

            if idx_list[0] is None:
                continue

            for jj in idx_list:
                collect_matches.append((ii, jj))

        return collect_matches

    @staticmethod
    def _parse_generators(op_dict, symmetries, generators):
        """
        Parse the generators of an Abelian combined group.

        **Returns**

        strides : dict
            With key being an irrep and the values being
            the coupling sector index, and the lower and
            upper value in a sub-matrix of the matrices.

        inds : integer array
            Result of argsort to permute matrices.

        link : instance of :class:`AbelianSymLink`
            Link according to the generator.
        """
        irreps = []
        for ii, key in enumerate(generators):
            elem = deepcopy(op_dict[key])
            # elem = key

            # Run check if generator is diagonal, real, and integers
            elem.assert_diagonal(tol=1e-14)
            elem.assert_real_valued(tol=1e-14)
            elem.assert_int_values(tol=1e-14)

            irrep_labels = elem.get_diag_entries_as_int()
            for irrep_label in irrep_labels:
                if irrep_label not in symmetries[ii]:
                    raise QRedTeaAbelianSymError(
                        "Irrep label from generator not part of symmetry."
                    )

            irreps.append(irrep_labels)

        sym = AbelianSymCombinedGroup(*symmetries)
        # sym = []
        # for elem in symmetries:
        #    sym.append(elem)

        # Transform to one row for charges
        irreps = iarray(irreps).transpose()

        inds = IrrepListing.argsort_irreps(irreps)

        strides = {}
        previous = None

        k1 = 0
        k2 = 0
        idx = None
        for ii in range(irreps.shape[0]):
            if previous is None:
                idx = ii
                previous = irreps[inds[ii], :]
                k2 += 1

            elif IrrepListing.is_equal_irrep(irreps[inds[ii], :], previous):
                k2 += 1

            else:
                strides[tuple(previous)] = (idx, k1, k2)
                k1 = k2
                k2 += 1
                idx += 1

                previous = irreps[inds[ii], :]

        strides[tuple(previous)] = (idx, k1, k2)

        irreps = irreps[inds, :]
        degeneracies = iones(irreps.shape[0])
        irrep_listing = IrrepListing.from_irreps(
            sym, irreps, degeneracies, are_sorted=True
        )

        link = AbelianSymLink(sym, irrep_listing)

        return strides, inds, link

    def _remove_duplicates(self):
        """
        Remove duplicate sectors by adding them to the first occurence.
        """
        tracker = {}
        nn = len(self.degeneracy_tensors)
        mask = bmaskt([nn])

        self.cs.generate_hashes(list(range(self.ndim)))

        for ii, sector in self.cs.iter_sectors():
            jj = tracker.get(tuple(sector), ii)

            if ii == jj:
                tracker[tuple(sector)] = ii
            else:
                mask[ii] = False
                self.degeneracy_tensors[jj].add_update(self.degeneracy_tensors[ii])

        if iall(mask):
            return self

        new_deg_tensors = []
        for ii, deg_tensor in enumerate(self.degeneracy_tensors):
            if mask[ii]:
                new_deg_tensors.append(deg_tensor)

        # Sorting is not affected, hashing becomes invalid as indices move
        cs = self.cs.denormalized_sectors[mask, :]
        sorted_for = self.cs.sorted_for
        self.cs = CouplingSectors(cs, sorted_for=sorted_for)
        self.degeneracy_tensors = new_deg_tensors

        if len(self.degeneracy_tensors) != self.cs.num_coupling_sectors:
            raise QRedTeaAbelianSymError("Mismatch cs and deg-tensor length.")

        if self.cs.num_coupling_sectors == 0:
            raise QRedTeaEmptyTensorError("Created empty tensors.")

        return self

    def _remove_trivial_irreps_on_link(self, link_idx):
        irrep_listing = IrrepListing.from_irreps(
            self.links[link_idx].sym,
            self.links[link_idx].irrep_listing.irreps,
            self.links[link_idx].irrep_listing.degeneracies,
            remove_trivial=True,
        )

        link_new = AbelianSymLink(self.links[link_idx].sym, irrep_listing)

        self._set_link(link_new, link_idx)

    def _set_link(self, link, link_idx):
        """Set a link a recalculated the coupling sectors."""
        for ii, cs in self.cs.iter_sectors():
            irrep = self.links[link_idx].irrep_listing.irreps[cs[link_idx], :]

            idx = link.irrep_listing.index(irrep, require_match=True)

            self.cs.denormalized_sectors[ii, link_idx] = idx

        self.links[link_idx] = link

        if self.cs.hashed_for is not None:
            if link_idx in self.cs.hashed_for:
                self.cs.hashed_for = None
                self.cs.hash_table = None

        if self.cs.sorted_for is not None:
            if link_idx in self.cs.sorted_for:
                self.cs.sorted_for = None

    def _split_links_with_fuse_rule(
        self, fuse_rule, link_idx, olinks, are_links_outgoing
    ):
        """
        **Arguments**

        self : instance of :class:`QteaAbelianTensor`
            Original tensor needed to access information of original links.

        fuse_rule : dict
            Information about fuse / split

        link_idx : integer
            Link to be split.

        olinks : list of integer
            Original links that have been fused.

        are_links_outgoing : list of booleans
            Link direction of ???

        **Returns**

        tensor : instance of :class:`QteaAbelianTensor`
            New tensor with previously fused link split now.
        """
        self.cs.generate_hashes([link_idx])

        deg_tensors = []
        cs_list = []

        for key, value in fuse_rule.items():
            if key in ["deg", "link", "deg_list"]:
                continue

            # New coupling sector and its lower and upper dimension
            cs_split_sub, k1, k2, old_shape = value

            # find index-list in current tensor
            idx_list = self.cs[(cs_split_sub,)]
            if idx_list[0] is None:
                raise QRedTeaAbelianSymError("Why is sector empty?")

            for ii in idx_list:
                if self.degeneracy_tensors[ii] is None:
                    # Nothing left
                    continue

                cs_fused = self.cs.denormalized_sectors[ii, :]
                cs_split = (
                    list(cs_fused[:link_idx])
                    + list(key)
                    + list(cs_fused[link_idx + 1 :])
                )

                tensor = self.degeneracy_tensors[ii]
                subtensor = tensor.subtensor_along_link(link_idx, k1, k2)

                shape = (
                    list(tensor.shape)[:link_idx]
                    + list(old_shape)
                    + list(tensor.shape)[link_idx + 1 :]
                )
                subtensor.reshape_update(shape)

                deg_tensors.append(subtensor)
                cs_list.append(cs_split)

        links = self.links[:link_idx] + olinks + self.links[link_idx + 1 :]
        outgoing = (
            self._are_links_outgoing[:link_idx]
            + are_links_outgoing
            + self._are_links_outgoing[link_idx + 1 :]
        )
        tensor = self._empty_from_links_directions(
            links, outgoing, self.base_tensor_cls
        )
        tensor._append_cs(deg_tensors, iarray(cs_list))

        return tensor

    def _split_prepare(self, legs_left, legs_right):
        """
        Prepare the split with any matrix decomposition.

        **Returns**

        split_tens : rank-2 tensor to run decomposition on.

        fuse_l : information for fuse and split rule (left link of split_tens)

        fuse_r : information for fuse and split rule (right link of split_tens)
        """
        if RUN_SANITY_CHECKS:
            for elem in self.links:
                elem.sanity_check()

        do_perm_in = imax(legs_left) >= imin(legs_right)
        if do_perm_in:
            perm_in = legs_left + legs_right
        else:
            # Still have to do this in case user reordered them (could check
            # on top here or adapt perm_left, perm_right strategy)
            perm_in = legs_left + legs_right

        split_tens = self.transpose(perm_in)
        split_tens, fuse_l, fuse_r = split_tens._fuse_links_for_split(len(legs_left))

        return split_tens, fuse_l, fuse_r

    def _split_finalize(
        self,
        split_tens,
        idx,
        legs,
        tensors,
        perm,
        is_q_link_outgoing,
        fuse_rule,
        new_deg=None,
    ):
        """
        Finalize a split by undoing the fusion of links.

        **Arguments**

        self : original incoming tensor, needed for links

        split_tens : fused rank-2 tensor

        idx : split index in tensors / split_tens

        legs : legs fused in original tensor `self`

        tensors : decomposed tensors

        perm : permutation on resulting tensor

        is_q_link_outgoing : flag if left tensor in decomposition
            has outgoing link

        fuse_rule : fuse rule generated by `_split_prepare`

        new_deg : new degeneracies in split link, e.g., after SVD
        """
        # By default summing over irreps, q-link will be outgoing, r-link will
        # be incoming. Will be modified before return
        outgoing = [False, True]
        outgoing[idx] = split_tens.are_links_outgoing[idx]

        if outgoing[0] or (not outgoing[1]):
            raise QRedTeaError("Double-check")

        links = split_tens.links.copy()

        tensor_rank2 = self._empty_from_links_directions(
            links, outgoing, self.base_tensor_cls
        )
        tensor_rank2._append_cs(tensors, split_tens.cs)

        olinks = [self.links[ii] for ii in legs]
        are_outgoing = [self._are_links_outgoing[ii] for ii in legs]
        tensor = tensor_rank2._split_links_with_fuse_rule(
            fuse_rule, idx, olinks, are_outgoing
        )

        link_idx = tensor.ndim - 1 if idx == 0 else 0
        tensor._set_link(fuse_rule["link"], link_idx)
        if not is_q_link_outgoing:
            tensor.flip_links_update([link_idx])

        if new_deg is not None:
            # Need to update degeneracy dimensions in link
            # Make sure link is free of trivial irreps with degeneracy zero

            slink_idx = 1 if idx == 0 else 0
            degeneracies = tensor.links[link_idx].irrep_listing.degeneracies.copy()

            for ii, cs_ii in split_tens.cs.iter_sectors():
                jj = cs_ii[slink_idx]
                irrep = split_tens.links[slink_idx].irrep_listing.irreps[jj, :]
                if not is_q_link_outgoing:
                    irrep = tensor.sym.invert_irrep(irrep)
                kk = tensor.links[link_idx].irrep_listing.index(
                    irrep, require_match=True
                )
                degeneracies[kk] = new_deg[ii]

            irrep_listing = IrrepListing.from_irreps(
                tensor.links[link_idx].sym,
                tensor.links[link_idx].irrep_listing.irreps,
                degeneracies,
                remove_trivial=False,
            )

            link = AbelianSymLink(split_tens.links[idx].sym, irrep_listing)
            tensor._set_link(link, link_idx)

        for ii in range(tensor.ndim):
            remove_trivial = tensor.links[ii].remove_trivial()
            if remove_trivial != tensor.links[ii]:
                tensor._remove_trivial_irreps_on_link(ii)

        if perm is not None:
            tensor.transpose_update(perm)

        if len(tensor.degeneracy_tensors) != tensor.cs.num_coupling_sectors:
            raise QRedTeaAbelianSymError("Mismatch cs and deg-tensor length.")

        if tensor.cs.num_coupling_sectors == 0:
            raise QRedTeaEmptyTensorError("Created empty tensors.")

        tensor.sanity_check()

        return tensor

    def _split_finalize_weights(
        self,
        split_tens,
        s_tensors,
        link,
        is_link_outgoing_left,
        allow_empty=False,
    ):
        cs = []
        filtered_s_tensors = []
        for ii, cs_ii in split_tens.cs.iter_sectors():
            if s_tensors[ii] is None:
                continue

            filtered_s_tensors.append(s_tensors[ii])
            jj = cs_ii[0]
            irrep = split_tens.links[0].irrep_listing.irreps[jj, :]
            if not is_link_outgoing_left:
                irrep = self.sym.invert_irrep(irrep)

            kk = link.irrep_listing.index(irrep, require_match=(not allow_empty))
            kk = -1 if kk is None else kk
            cs.append(kk)

        cs = iarray(cs)
        cs = cs.reshape([len(cs), 1])
        weights = AbelianSymLinkWeight(
            link, cs, filtered_s_tensors, self.base_tensor_cls, allow_empty=allow_empty
        )

        return weights

    def _to_vector(self, mapping):
        """Use a mapping to fill vector with entries of symmetric tensor."""
        if RUN_SANITY_CHECKS:
            self.sanity_check()

        if self.cs.num_coupling_sectors == 0:
            raise QRedTeaEmptyTensorError("Trying to map empty tensor to vector.")

        vec = self.degeneracy_tensors[0].vector_with_dim_like(mapping["dim"])

        for ii, cs_ii in self.cs.iter_sectors():
            key = tuple(cs_ii)

            if key in mapping:
                k1, k2, _ = mapping[tuple(cs_ii)]
                vec[k1:k2] = self.degeneracy_tensors[ii].flatten()

        return vec

    @staticmethod
    def _synchronize_streams(streams):
        """Wait for all streams in the list to synchronize."""
        # Synchronize all streams to ensure order
        for stream in streams:
            if not isinstance(stream, nullcontext):
                stream.synchronize()

    def _trivial_fuse_links(self, fuse_low, fuse_high, is_link_outgoing):
        """Trivial fuse with all links being of dimension one."""

        link = self.links[0].from_link_list(
            self.links[fuse_low : fuse_high + 1],
            self._are_links_outgoing[fuse_low : fuse_high + 1],
        )

        cs_fused = self.cs.denormalized_sectors[:, fuse_low : fuse_high + 1]
        if isum(cs_fused) != 0:
            raise QRedTeaAbelianSymError("No trivial fuse links case.")

        irrep = self.links[fuse_low].select_irreps(0)
        if self._are_links_outgoing[fuse_low]:
            irrep = self.links[fuse_low].sym.invert_irrep(irrep)

        for ii in range(fuse_low + 1, fuse_high + 1):
            irrep_b = self.links[ii].select_irreps(0)

            if self._are_links_outgoing[ii]:
                irrep_b = self.links[ii].sym.invert_irrep(irrep_b)

            irrep = self.links[ii].sym.couple_irreps(irrep, irrep_b)

        idx = link.irrep_listing.index(irrep)
        if idx != 0:
            raise QRedTeaAbelianSymError("No trivial fuse links case.")

        for _ in range(fuse_low, fuse_high + 1):
            self.links.pop(fuse_low)
            self._are_links_outgoing.pop(fuse_low)

        if is_link_outgoing:
            link = link.invert()

        self.links.insert(fuse_low, link)
        self._are_links_outgoing.insert(fuse_low, is_link_outgoing)

        # Adapt coupling sectors
        nn = self.cs.num_coupling_sectors
        cs = izeros((nn, len(self.links)))

        cs[:, :fuse_low] = self.cs.denormalized_sectors[:, :fuse_low]
        cs[:, fuse_low + 1 :] = self.cs.denormalized_sectors[:, fuse_high + 1 :]

        self.cs = CouplingSectors(cs)

        # Fuse degeneracy tensors
        for elem in self.degeneracy_tensors:
            elem.fuse_links_update(fuse_low, fuse_high)

        self.sanity_check()

        return self

    def print_full(self, indent=0, tag=""):
        """Print all information on tensor."""
        prefix = " " * indent
        prefix4 = " " * (indent + 4)
        prefix8 = " " * (indent + 8)
        print(prefix + "=" * 10 + " AbelianTensor %s " % (tag) + "=" * 10)
        print(prefix + "Ran:", self.ndim)
        print(prefix + "Link direction", self._are_links_outgoing)
        print(prefix + "Links:")
        for link in self.links:
            link.print_full(indent=indent + 4)

        print(prefix + "CS")
        for ii, elem in self.cs.iter_sectors():
            print(prefix4 + "norm:", self.degeneracy_tensors[ii].norm())
            print(prefix4 + "CS", ii, "indices", elem)
            for jj in range(self.ndim):
                print(
                    prefix8 + "link",
                    jj,
                    "irreps:",
                    self.links[jj].irrep_listing.irreps[elem[jj], :],
                )
        print(prefix + "^" * 34)


#    def _deprecated_split_finalize_left(
#        self, split_tens, legs_left, left_tensors, perm_left, is_q_link_outgoing, fuse_l
#    ):
#        # By default summing over irreps, q-link will be outgoing, r-link will
#        # be incoming. Will be modified before return
#        q_outgoing = [split_tens.are_links_outgoing[0], True]

#        q_tensor_rank2 = self._empty_from_links_directions(split_tens.links, q_outgoing)
#        q_tensor_rank2._append_cs(left_tensors, split_tens.cs)

#        olinks = [self.links[ii] for ii in legs_left]
#        are_outgoing = [self._are_links_outgoing[ii] for ii in legs_left]
#        q_tensor = q_tensor_rank2._split_links_with_fuse_rule(
#        #    fuse_l, 0, olinks, are_outgoing
#        )

#        if not is_q_link_outgoing:
#        #    link_idx = q_tensor.ndim - 1
#        #    q_tensor.links = q_tensor._invert_link_selection([link_idx])
#        #    q_tensor.are_links_outgoing[link_idx] = False

#        if perm_left is not None:
#        #    q_tensor.transpose_update(perm_left)

#        if len(q_tensor.degeneracy_tensors) != q_tensor.cs.num_coupling_sectors:
#        #    raise QRedTeaAbelianSymError("Mismatch cs and deg-tensor length.")

#        if q_tensor.cs.num_coupling_sectors == 0:
#        #    raise QRedTeaEmptyTensorError("Created empty tensors.")

#        return q_tensor

#    def _deprecated_split_finalize_right(
#        self,
#        split_tens,
#        legs_right,
#        right_tensors,
#        perm_right,
#        is_q_link_outgoing,
#        fuse_r,
#    ):
#        # By default summing over irreps, q-link will be outgoing, r-link will
#        # be incoming. Will be modified before return
#        r_outgoing = [False, split_tens.are_links_outgoing[1]]

#        r_tensor_rank2 = self._empty_from_links_directions(split_tens.links, r_outgoing)
#        r_tensor_rank2._append_cs(right_tensors, split_tens.cs)

#        olinks = [self.links[ii] for ii in legs_right]
#        are_outgoing = [self._are_links_outgoing[ii] for ii in legs_right]
#        r_tensor = r_tensor_rank2._split_links_with_fuse_rule(
#        #    fuse_r, 1, olinks, are_outgoing
#        )

#        if not is_q_link_outgoing:
#        #    link_idx = 1
#        #    r_tensor.links = r_tensor._invert_link_selection([link_idx])
#        #    r_tensor.are_links_outgoing[link_idx] = True

#        if perm_right is not None:
#        #    r_tensor.transpose_update(perm_right)

#        if len(r_tensor.degeneracy_tensors) != r_tensor.cs.num_coupling_sectors:
#        #    raise QRedTeaAbelianSymError("Mismatch cs and deg-tensor length.")

#        if r_tensor.cs.num_coupling_sectors == 0:
#        #    raise QRedTeaEmptyTensorError("Created empty tensors.")

#        return r_tensor

#    def deprecated_couple_links(self):
#        irrep = self.links[0].irrep_listing
#        inv_a = self._are_links_outgoing[0]

#        for ii in range(1, self.ndim - 1):
#            inv_b = self._are_links_outgoing[ii]
#            irrep = irrep.product_couple(self.links[ii].irrep_listing, inv_a, inv_b)

#            # Never invert after first iteration as it are merged irreps
#            inv_a = False

# Find matching irreps


class AbelianSymmetryInjector:
    """
    Provide a way to inject parsing of symmetry, i.e., generator, trivial
    symmetries etc.
    """

    @staticmethod
    def inject_parse_symmetries(params):
        """
        Function used to inject the parsing of the symmetry from the params
        into a tensor backend.

        **Arguments**

        params : dict
            Dictionary with simulation params, of interest are here
            the keys `SymmetryTypes` and `Symmetries`.

        **Returns**

        sym : :class:`AbelianSymCombinedGroup`
        """
        if ("SymmetryTypes" in params) and ("Symmetries" not in params):
            sym = []
            for elem in params["SymmetryTypes"]:
                if elem == "U":
                    sym.append(AbelianSymU1())
                elif elem.startswith("Z"):
                    order = int(elem.replace("Z", ""))
                    sym.append(AbelianSymZN(order))
                else:
                    raise QRedTeaAbelianSymError(f"Failed parsing symmetry {elem}.")
            sym = AbelianSymCombinedGroup(sym)
        elif "Symmetries" in params:
            sym = AbelianSymCombinedGroup(params["Symmetries"])
        else:
            raise QRedTeaAbelianSymError("Do not know how to parse this.")

        return sym

    @staticmethod
    def inject_trivial_symmetry():
        """
        Use the Abelian U(1) symmetry as trivial symmetry with one-block.

        **Returns**

        sym : :class:`AbelianSymCombinedGroup`
        """
        return AbelianSymCombinedGroup(AbelianSymU1())

    # This could be a static method, but inheriting classes not necessarily,
    # so we prefer to have them all equal as class methods; nobody should
    # be relying right now on calling it on the type itself
    def inject_parse_sectors(self, params, sym):
        """
        Parse sectors for symmetry and update symmetry if necessary.

        **Arguments**

        params : dict
            Dictionary with simulation params, of interest are here
            the keys `SymmetryTypes` and `Symmetries`.

        **Returns**

        sym : :class:`AbelianSymCombinedGroup`

        sectors : dict
            Dictionary with positions as key and irreps as values.

        **Details**

        The position is hard-coded for the TTN at the moment.
        """
        if "SymmetrySectors" in params:
            irrep = np.array(params["SymmetrySectors"])
        else:
            # Set trivial sector
            warnings.warn("Selecting trival sector because not present.")
            nn = max(1, len(sym))
            irrep = np.zeros(nn, dtype=int)

        if sym:
            tmp_sym = sym
        else:
            # Also define trivial symmetry
            tmp_sym = AbelianSymCombinedGroup(AbelianSymU1())

        irrep = irrep.reshape([1] + [len(irrep)])
        sectors = {
            "global": IrrepListing.from_irreps(tmp_sym, irrep, np.ones(1, dtype=int)),
            # Deprecated (0, 0) as it works only for TTN
            (0, 0): IrrepListing.from_irreps(tmp_sym, irrep, np.ones(1, dtype=int)),
        }

        return tmp_sym, sectors


def default_abelian_backend(device="cpu", dtype=np.complex128):
    """
    Generate a default tensor backend for symmetric tensors, i.e., with
    a :class:`QteaTensor`.

    **Arguments**

    dtype : data type, optional
        Data type for numpy or cupy.
        Default to np.complex128

    device : device specification, optional
        Default to `"cpu"`.
        Available: `"cpu", "gpu"`

    **Returns**

    tensor_backend : :class:`TensorBackend`
    """
    tensor_backend = TensorBackend(
        tensor_cls=QteaAbelianTensor,
        base_tensor_cls=QteaTensor,
        device=device,
        dtype=dtype,
        symmetry_injector=AbelianSymmetryInjector(),
        datamover=QteaTensor.get_default_datamover(),
    )

    return tensor_backend
