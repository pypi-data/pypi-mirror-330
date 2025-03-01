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
Tensor class based on pytorch; pytorch supports both CPU and GPU in one framework.
"""

# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-statements
# pylint: disable=wrong-import-position

import gc
import itertools
import logging
import math
from contextlib import nullcontext

import numpy as np

# All imports cause problems for the build server at the moment
# * torch is simply not install
# * qtealeaves is lost in the conan generator somewhere
from qtealeaves.tooling.devices import _CPU_DEVICE, _GPU_DEVICE, _XLA_DEVICE, DeviceList
from qtealeaves.tooling.mpisupport import MPI, TN_MPI_TYPES

# pylint: disable-next=wrong-import-order,ungrouped-imports
from qredtea.tooling import QRedTeaBackendLibraryImportError

try:
    import torch as to
except ImportError as exc:
    raise QRedTeaBackendLibraryImportError() from exc
GPU_AVAILABLE = to.cuda.is_available()
try:
    # pylint: disable-next=unused-import
    import torch_xla

    # Okay, this is a bold assumption, but how to get the device count?
    XLA_AVAILABLE = True
    import torch_xla.core.xla_model as xm

    # xla_device is global variable, similar to GPU, we cannot select
    # a specific device if multiple are avaiable.
    # pylint: disable-next=invalid-name
    xla_device = xm.xla_device()
except ImportError:
    XLA_AVAILABLE = False
    # pylint: disable-next=invalid-name
    xla_device = None

# pylint: disable=import-error,ungrouped-imports,no-name-in-module
from qtealeaves.convergence_parameters import TNConvergenceParameters
from qtealeaves.operators import TNOperators
from qtealeaves.solvers import EigenSolverH
from qtealeaves.tensors import (
    QteaTensor,
    TensorBackend,
    _AbstractDataMover,
    _AbstractQteaBaseTensor,
    _parse_block_size,
    _process_svd_ctrl,
)
from qtealeaves.tooling import write_tensor

from qredtea.symmetries import AbelianSymmetryInjector, QteaAbelianTensor
from qredtea.tooling import (
    QRedTeaError,
    QRedTeaLinAlgError,
    QRedTeaLinkError,
    QRedTeaRankError,
)

# pylint: enable=import-error,ungrouped-imports,no-name-in-module

ACCELERATOR_DEVICES = DeviceList([_GPU_DEVICE, _XLA_DEVICE])

# pylint: disable-next=invalid-name
_BLOCK_SIZE_BOND_DIMENSION, _BLOCK_SIZE_BYTE = _parse_block_size()

# pylint: disable-next=invalid-name
_USE_STREAMS = False


__all__ = [
    "QteaTorchTensor",
    "default_pytorch_backend",
    "default_abelian_pytorch_backend",
    "set_block_size_qteatorchtensors",
    "get_gpu_available",
    "DataMoverPytorch",
]

logger = logging.getLogger(__name__)


def get_gpu_available():
    """Returns boolean on availability of GPU."""
    return GPU_AVAILABLE


def set_block_size_qteatorchtensors(
    block_size_bond_dimension=None, block_size_byte=None
):
    """
    Allows to overwrite bond dimension decisions to enhance performance
    on hardware by keeping "better" or "consistent" bond dimensions.
    Only one of the two can be used right now.

    **Arguments**

    block_size_bond_dimension : int
        Direct handling of bond dimension.

    block_size_byte : int
        Control dimension of tensors (in SVD cuts) via blocks of bytes.
        For example, nvidia docs suggest multiples of sixteen float64
        or 32 float32 for A100, i.e., 128 bytes.
    """
    # pylint: disable-next=invalid-name,global-statement
    global _BLOCK_SIZE_BOND_DIMENSION
    # pylint: disable-next=invalid-name,global-statement
    global _BLOCK_SIZE_BYTE

    _BLOCK_SIZE_BOND_DIMENSION = block_size_bond_dimension
    _BLOCK_SIZE_BYTE = block_size_byte

    if (block_size_bond_dimension is not None) and (block_size_byte is not None):
        # We do not want to handle both of them, will be ignored lateron,
        # but raise warning as early as possible
        logger.warning(
            "Ignoring BLOCK_SIZE_BOND_DIMENSION in favor of BLOCK_SIZE_BYTE."
        )


def set_streams_qteatorchtensors(use_streams):
    """
    Allow to decide if streams are used.

    **Arguments**

    use_streams : bool
        If True, streams will be used, otherwise we return a nullcontext even
        if streams would be possible.

    """
    # pylint: disable-next=invalid-name,global-statement
    global _USE_STREAMS

    _USE_STREAMS = use_streams


# class set_block_size_qteatorchtensors once to resolve if both variables
# are set
set_block_size_qteatorchtensors(_BLOCK_SIZE_BOND_DIMENSION, _BLOCK_SIZE_BYTE)


class QteaTorchStream(to.cuda.StreamContext):
    # pylint: disable=too-few-public-methods
    """
    Wrapper for stream with torch which provides access to synchronize.
    """

    def __init__(self):
        self.stream = to.cuda.Stream()
        super().__init__(self.stream)

    def synchronize(self, *args, **kwargs):
        """Synchronize the stream used within the instance."""
        self.stream.synchronize()


class QteaTorchTensor(_AbstractQteaBaseTensor):
    """
    Tensor for Quantum TEA based on the pytorch tensors.
    """

    implemented_devices = DeviceList([_CPU_DEVICE, _GPU_DEVICE, _XLA_DEVICE])

    def __init__(
        self,
        links,
        ctrl="Z",
        are_links_outgoing=None,  # pylint: disable=unused-argument
        base_tensor_cls=None,  # pylint: disable=unused-argument
        dtype=to.complex128,
        device=None,
        requires_grad=None,
    ):
        """

        links : list of ints with shape (links works towards generalization)
        """
        super().__init__(links)

        if ctrl is None:
            self._elem = None
            return

        if requires_grad is None:
            requires_grad = False
        if ctrl in ["N"]:
            self._elem = to.empty(links, dtype=dtype, requires_grad=requires_grad)
        elif ctrl in ["O"]:
            self._elem = to.ones(links, dtype=dtype, requires_grad=requires_grad)
        elif ctrl in ["Z"]:
            self._elem = to.zeros(links, dtype=dtype, requires_grad=requires_grad)
        elif ctrl in ["1", "eye"]:
            if len(links) != 2:
                raise ValueError("Initialization with identity only for rank-2.")
            if links[0] != links[1]:
                raise ValueError("Initialization with identity only for square matrix.")
            self._elem = to.eye(links[0], dtype=dtype, requires_grad=requires_grad)
        elif ctrl in ["R", "random"]:
            if dtype in [to.complex64, to.complex128]:
                self._elem = to.rand(
                    *links, requires_grad=requires_grad
                ) + 1j * to.rand(*links, requires_grad=requires_grad)
            else:
                self._elem = to.rand(*links, requires_grad=requires_grad)
        elif ctrl in ["ground"]:
            dim = int(to.prod(to.Tensor(links)).item())
            self._elem = to.zeros([dim], dtype=dtype)
            self._elem[0] = 1.0
            self._elem = to.reshape(self._elem, links)
            self._elem.requires_grad_(requires_grad)
        elif np.isscalar(ctrl) and np.isreal(ctrl):
            # This prohibits initialization with complex numbers.
            # In case of adding complex numbers, enforce a complex dtype!
            self._elem = ctrl * to.ones(links, dtype=dtype, requires_grad=requires_grad)
        else:
            raise QRedTeaError(f"Unknown initialization {ctrl} of type {type(ctrl)}.")

        self.convert(dtype, device)

        if (not self._elem.is_leaf) and (requires_grad):
            self._elem = self.elem.detach().clone().requires_grad_(True)

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    def are_links_outgoing(self):
        """Define property of outgoing links as property (always False)."""
        return [False] * self.ndim

    @property
    def device(self):
        """Device where the tensor is stored."""
        return self.device_str(self._elem)

    @property
    def elem(self):
        """Elements of the tensor."""
        return self._elem

    @property
    def dtype(self):
        """Data type of the underlying arrays."""
        return self._elem.dtype

    @property
    def dtype_eps(self):
        """Data type's machine precision."""
        eps_dict = {
            "torch.float16": 1e-3,
            "torch.float32": 1e-7,
            "torch.float64": 1e-14,
            "torch.complex64": 1e-7,
            "torch.complex128": 1e-14,
        }

        return eps_dict[str(self.dtype)]

    @property
    def linear_algebra_library(self):
        """Specification of the linear algebra library used as string `torch``."""
        return "torch"

    @property
    def links(self):
        """Here, as well dimension of tensor along each dimension."""
        return self.shape

    @property
    def ndim(self):
        """Rank of the tensor."""
        return self._elem.ndim

    @property
    def shape(self):
        """Dimension of tensor along each dimension."""
        return tuple(self._elem.shape)

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
        new_tensor = self.copy()
        if isinstance(other, QteaTorchTensor):
            if self.elem.requires_grad:
                # torch backpropagation dislikes in-place operations.
                new_tensor._elem = new_tensor.elem + other.elem
            else:
                new_tensor._elem += other.elem
        elif not to.is_tensor(other):
            # Assume it is scalar then
            new_tensor._elem += other
        else:
            raise TypeError(
                "Addition for QteaTensor is defined only for scalars and QteaTensor,"
                + f" not {type(other)}"
            )
        return new_tensor

    def __iadd__(self, other):
        """In-place addition of tensor with tensor or scalar (update)."""
        if isinstance(other, QteaTorchTensor):
            self._elem += other.elem
        elif not to.is_tensor(other):
            # Assume it is scalar then
            self._elem += other
        else:
            raise TypeError(
                "Addition for QteaTorchTensor is defined only for scalars"
                + f" and QteaTorchTensor, not {type(other)}"
            )
        return self

    def __mul__(self, factor):
        """Multiplication of tensor with scalar returning new tensor as result."""
        return self.from_elem_array(
            factor * self._elem, dtype=self.dtype, device=self.device
        )

    def __matmul__(self, other):
        """Matrix multiplication as contraction over last and first index of self and other."""
        idx = self.ndim - 1
        return self.tensordot(other, ([idx], [0]))

    def __imul__(self, factor):
        """In-place multiplication of tensor with scalar (update)."""
        self._elem *= factor
        return self

    def __itruediv__(self, factor):
        """In-place division of tensor with scalar (update)."""
        if factor == 0:
            raise ZeroDivisionError("Trying to divide by zero.")
        self._elem /= factor
        return self

    def __sub__(self, other):
        """
        Subtraction of a scalar to a tensor subtracts it to all the entries.
        If other is another tensor, elementwise subtraction if they have the same shape
        """
        new_tensor = self.copy()
        if isinstance(other, QteaTorchTensor):
            new_tensor._elem -= other.elem
        elif not to.is_tensor(other):
            # Assume it is scalar then
            new_tensor._elem -= other
        else:
            raise TypeError(
                "Subtraction for QteaTorchTensor is defined only for scalars"
                + f" and QteaTorchTensor, not {type(other)}"
            )
        return new_tensor

    def __truediv__(self, factor):
        """Division of tensor with scalar."""
        if factor == 0:
            raise ZeroDivisionError("Trying to divide by zero.")
        elem = self._elem / factor
        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def __neg__(self):
        """Negative of a tensor returned as a new tensor."""
        # pylint: disable-next=invalid-unary-operand-type
        neg_elem = -self._elem
        return self.from_elem_array(neg_elem, dtype=self.dtype, device=self.device)

    # --------------------------------------------------------------------------
    #                       classmethod, classmethod like
    # --------------------------------------------------------------------------

    @staticmethod
    def convert_operator_dict(
        op_dict,
        params=None,
        symmetries=None,
        generators=None,
        base_tensor_cls=None,
        dtype=to.complex128,
        device=_CPU_DEVICE,
    ):
        """
        Iterate through an operator dict and convert the entries. Converts as well
        to rank-4 tensors.

        **Arguments**

        op_dict : instance of :class:`TNOperators`
            Contains the operators as xp.ndarray.

        params : dict, optional
            To resolve operators being passed as callable.

        symmetries:  list, optional, for compatability with symmetric tensors.
            Must be empty list.

        generators : list, optional, for compatability with symmetric tensors.
            Must be empty list.

        base_tensor_cls : None, optional, for compatability with symmetric tensors.
            No checks on this one here.

        dtype : data type for xp, optional
            Specify data type.
            Default to `to.complex128`

        device : str
            Device for the simulation. Available "cpu" and "gpu"
            Default to "cpu"

        **Details**

        The conversion to rank-4 tensors is useful for future implementations,
        either to support adding interactions with a bond dimension greater than
        one between them or for symmetries. We add dummy links of dimension one.
        The order is (dummy link to the left, old link-1, old link-2, dummy link
        to the right).
        """
        qteatensor_dict = QteaTensor.convert_operator_dict(
            op_dict,
            params=params,
            symmetries=symmetries,
            generators=generators,
            base_tensor_cls=base_tensor_cls,
            dtype=np.complex128,
            device=_CPU_DEVICE,
        )

        new_op_dict = TNOperators(
            set_names=qteatensor_dict.set_names,
            mapping_func=qteatensor_dict.mapping_func,
        )
        for key, value in qteatensor_dict.items():
            new_op_dict[key] = QteaTorchTensor.from_qteatensor(value)
            new_op_dict[key].convert(dtype, device)

        return new_op_dict

    def copy(self, dtype=None, device=None):
        """Make a copy of a tensor; using detach and clone and keeping the requires grad option"""
        if dtype is None:
            dtype = self.dtype
        if device is None:
            device = self.device

        if self.elem.requires_grad:
            return self.from_elem_array(self._elem.clone(), dtype=dtype, device=device)

        return self.from_elem_array(
            self._elem.clone().detach(), dtype=dtype, device=device
        )

    def eye_like(self, link):
        """
        Generate identity matrix.

        **Arguments**

        self : instance of :class:`QteaTensor`
            Extract data type etc from this one here.

        link : same as returned by `links` property, here integer.
            Dimension of the square, identity matrix.
        """
        elem = to.eye(link)
        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    @classmethod
    def from_qteatensor(cls, qteatensor, dtype=None, device=None):
        """Convert QteaTensor based on numpy/cupy into QteaTorchTensor."""
        elem = to.from_numpy(qteatensor.elem)
        return cls.from_elem_array(elem, dtype=dtype, device=device)

    def random_unitary(self, link):
        """
        Generate a random unitary matrix via performing a SVD on a
        random tensor.

        **Arguments**

        self : instance of :class:`QteaTensor`
            Extract data type etc from this one here.

        link : same as returned by `links` property, here integer.
            Dimension of the square, random unitary matrix.
        """
        elem = to.rand(link, link)
        elem, _, _ = to.linalg.svd(elem, full_matrices=False)

        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    @classmethod
    def read(cls, filehandle, dtype, device, base_tensor_cls, cmplx=True, order="F"):
        """Read a tensor from file via QteaTensor."""
        qteatensor = QteaTensor.read(
            filehandle,
            np.complex128,
            _CPU_DEVICE,
            base_tensor_cls,
            cmplx=cmplx,
            order=order,
        )
        obj = cls.from_qteatensor(qteatensor)
        obj.convert(dtype, device)
        return obj

    @staticmethod
    # pylint: disable-next=unused-argument
    def dummy_link(example_link):
        """Return a dummy link which is always an int for base tensors."""
        return 1

    @staticmethod
    def set_missing_link(links, max_dim, are_links_outgoing=None):
        """
        Calculate the property of a missing link in a list.

        **Arguments**

        links : list
            Contains data like returned by property `links`, except
            for one element being `None`

        max_dim : int
            Maximal dimension of link allowed by convergence parameters
            or similar.

        are_links_outgoing : list of bools
            Indicates link direction for symmetry tensors only.
        """
        return QteaTensor.set_missing_link(
            links, max_dim, are_links_outgoing=are_links_outgoing
        )

    def zeros_like(self, requires_grad=False):
        """Get a tensor same as `self` but filled with zeros."""
        return type(self)(
            self.shape,
            ctrl="Z",
            dtype=self.dtype,
            device=self.device,
            requires_grad=requires_grad,
        )

    def identity_like(self, fuse_point, requires_grad=False):
        """Get an identity for the legs fused as: (0, fuse_point),(fuse_point+1,...).
        Same shape as `self`."""
        mat = self.copy()

        # fuse legs
        mat.fuse_links_update(0, fuse_point)
        mat.fuse_links_update(1, mat.ndim - 1)
        # make identity
        identity = type(self)(
            mat.shape,
            ctrl="1",
            dtype=self.dtype,
            device=self.device,
            requires_grad=requires_grad,
        )
        # reshape back into the original shape
        identity.reshape_update(self.shape)
        return identity

    # --------------------------------------------------------------------------
    #                            Checks and asserts
    # --------------------------------------------------------------------------
    #
    # inherit def assert_normalized
    # inherit def assert_unitary
    # inherit def sanity_check

    def are_equal(self, other, tol=1e-7):
        """Check if two tensors are equal."""
        if self.ndim != other.ndim:
            return False

        if np.any(self.shape != other.shape):
            return False

        return to.isclose(self._elem, other.elem, atol=tol).all().item()

    def assert_identical_irrep(self, link_idx):
        """Assert that specified link is identical irreps."""
        if self.shape[link_idx] != 1:
            raise QRedTeaLinkError("Link dim is greater one in identical irrep check.")

    def assert_identity(self, tol=1e-7):
        """Check if tensor is an identity matrix."""

        if not self.is_close_identity(tol=tol):
            logger.error("Error information tensor:\n%s", self._elem)
            raise QRedTeaError("Tensor not diagonal with ones.")

    def is_close_identity(self, tol=1e-7):
        """Check if rank-2 tensor is close to identity."""
        if self.ndim != 2:
            return False

        if self.shape[0] != self.shape[1]:
            return False

        eye = to.eye(self.shape[0], device=self._elem.device)
        eps = (to.abs(eye - self._elem)).max().item()

        return eps < tol

    def is_implemented_device(self, query):
        """
        Check if argument query is an implemented device.

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
        return query in self.implemented_devices

    @staticmethod
    def is_xla_static(device_str):
        """
        Check if device is XLA or not.

        Parameters
        ----------

        device_str : str
            Check for this string if it is a XLA device.

        Returns
        -------

        is_xla : bool
            True if device is a XLA.
        """
        return device_str.startswith(_XLA_DEVICE)

    def is_xla(self, query=None):
        """
        Check if device is XLA or not.

        Parameters
        ----------

        query : str | None, optional
            If given, check for this string. If `None`, self.device
            will be checked.
            Default to None.

        Returns
        -------

        is_xla : bool
            True if device is a XLA.

        """
        return self.is_xla_static(self.device if query is None else query)

    def is_dtype_complex(self):
        """Check if data type is complex."""
        return self._elem.is_complex()

    def is_link_full(self, link_idx):
        """Check if the link at given index is at full bond dimension."""
        links = list(self.links)
        links[link_idx] = None

        links = self.set_missing_link(links, None)

        return self.links[link_idx] >= links[link_idx]

    # --------------------------------------------------------------------------
    #                       Single-tensor operations
    # --------------------------------------------------------------------------
    #
    # inherit def flip_links_update

    # pylint: disable-next=unused-argument
    def attach_dummy_link(self, position, is_outgoing=True):
        """Attach dummy link at given position (inplace update)."""
        self.reshape_update(self._attach_dummy_link_shape(position))
        return self

    def conj(self):
        """Return the complex conjugated in a new tensor."""
        # For both real and complex tensors, conj() does not (always?)
        # return a true copy, but the "same memory address" which means
        # inplace-updates on the conjugate tensor modify the original self.

        # Educated guess: Assuming gradients shoud be preserved in such a
        # case, return a clone() and not a detach().clone()
        if self._elem.is_complex():
            return self.from_elem_array(
                self._elem.clone().conj(), dtype=self.dtype, device=self.device
            )

        return self.from_elem_array(
            self._elem.clone(), dtype=self.dtype, device=self.device
        )

    def conj_update(self):
        """Apply the complex conjugated to the tensor in place."""
        to.conj(self._elem, out=self._elem)

    def _convert_check(self, device):
        """Run check that device is implemented and available."""
        if device is not None:
            if device not in self.implemented_devices:
                raise ValueError(
                    f"Device {device} is not implemented. Select from"
                    + f" {self.implemented_devices}"
                )
            if self.is_gpu(query=device) and (not GPU_AVAILABLE):
                raise ImportError("CUDA GPU is not available")
            if self.is_xla(query=device) and (not XLA_AVAILABLE):
                raise ImportError("XLA is not available.")

    # pylint: disable-next=unused-argument
    def convert(self, dtype=None, device=None, stream=None):
        """Convert underlying array to the specified data type inplace."""
        # Both devices available, figure out what we currently have
        # and start converting
        current = self.device

        if self.is_xla() or self.is_xla(query=device):
            # Conversion causes problem if data types are converted
            # on xla device, handle conversion in separate function
            return self._xla_convert(dtype, device, stream)

        if device is not None:
            self._convert_check(device)

            if device == current:
                # We already are in the correct device
                pass
            elif self.is_gpu(query=device):
                # We go from the cpu to gpu
                cuda_str = device.replace(_GPU_DEVICE, "cuda")
                self._elem = self._elem.to(device=cuda_str)
            elif self.is_cpu(query=device):
                # We go from gpu to cpu
                self._elem = self._elem.to(device=_CPU_DEVICE)
            else:
                # CPU to XLA has to go here once not covered in special case
                raise QRedTeaError(
                    f"Conversion {current} to {device} not possible or not considered yet."
                )

        if (dtype is not None) and (dtype != self.dtype):
            self._elem = self._elem.type(dtype)

        return self

    def convert_singvals(self, singvals, dtype, device):
        """Convert the singular values via a tensor."""
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global xla_device

        if device is not None:
            self._convert_check(device)

            # Both devices available, figure out what we currently have
            # and start converting
            current = self.device

            if device == current:
                # We already are in the correct device
                pass
            elif self.is_gpu(query=device):
                # We go to the cpu to gpu
                cuda_str = device.replace(_GPU_DEVICE, "cuda")
                singvals = singvals.to(device=cuda_str)
            elif self.is_cpu(query=device):
                # We go from gpu to cpu
                singvals = singvals.to(device=_CPU_DEVICE)
            elif self.is_xla(query=device):
                # We go from the cpu to xla
                singvals = singvals.to(device=xla_device)

        if dtype is not None:
            dtype = {
                "torch.float16": to.float16,
                "torch.float32": to.float32,
                "torch.float64": to.float64,
                "torch.complex32": to.float16,
                "torch.complex64": to.float32,
                "torch.complex128": to.float64,
            }[str(self.dtype)]

            if dtype != singvals.dtype:
                singvals = singvals.to(dtype)
        return singvals

    def diag(self, real_part_only=False, do_get=False):
        """Return the diagonal as array of rank-2 tensor."""
        if self.ndim != 2:
            raise QRedTeaRankError("Can only run on rank-2.")

        diag = self._elem.diag()

        if real_part_only and diag.is_complex():
            diag = to.real(diag)

        if self.device in ACCELERATOR_DEVICES and do_get:
            diag = diag.to(device=_CPU_DEVICE)

        return diag

    def dtype_from_char(self, dtype):
        """Resolve data type from chars C, D, S, Z and optionally H."""
        data_types = {
            "A": to.complex128,
            "C": to.complex64,
            "D": to.float64,
            "H": to.float16,
            "S": to.float32,
            "Z": to.complex128,
            "I": to.int32,
        }

        return data_types[dtype]

    def eig_api(
        self, matvec_func, links, conv_params, args_func=None, kwargs_func=None
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

        eigenvectors : instance of :class:`QteaTensor`
        """
        eig_api_no_arpack = True
        eig_api_qtea_half = self.dtype == to.float16

        # scipy eigsh switches for complex data types to eigs and
        # can only solve k eigenvectors of a nxn matrix with
        # k < n - 1. This leads to problems with 2x2 matrices
        # where one can get not even one eigenvector.
        eig_api_qtea_dim2 = self.is_dtype_complex() and (np.prod(self.shape) == 2)

        if eig_api_qtea_half or eig_api_qtea_dim2 or eig_api_no_arpack:
            val, vec = self.eig_api_qtea(
                matvec_func,
                conv_params,
                args_func=args_func,
                kwargs_func=kwargs_func,
            )

            # Half precision had problems with normalization (most likely
            # as eigh is executed on higher precision
            vec /= vec.norm_sqrt()

            return val, vec

        return self.eig_api_arpack(
            matvec_func,
            links,
            conv_params,
            args_func=args_func,
            kwargs_func=kwargs_func,
        )

    def eig_api_qtea(self, matvec_func, conv_params, args_func=None, kwargs_func=None):
        """
        Interface to hermitian eigenproblem via qtealeaves.solvers. Arguments see `eig_api`.
        """
        solver = EigenSolverH(
            self,
            matvec_func,
            conv_params,
            args_func=args_func,
            kwargs_func=kwargs_func,
        )

        return solver.solve()

    def eig_api_arpack(
        self, matvec_func, links, conv_params, args_func=None, kwargs_func=None
    ):
        """
        Interface to hermitian eigenproblem via Arpack. Arguments see `eig_api`.
        Possible implementation is https://github.com/rfeinman/Torch-ARPACK.
        """
        raise NotImplementedError("Arpack is non-default interface for pytorch.")

    def einsum(self, einsum_str, *others):
        """
        Call to einsum with `self` as first tensor.

        Arguments
        ---------

        einsum_str : str
            Einsum contraction rule.

        other: List[:class:`QteaTorchTensors`]
            2nd, 3rd, ..., n-th tensor in einsum rule as
            positional arguments.

        Results
        -------

        tensor : :class:`QteaTorchTensor`
            Contracted tensor according to the einsum rules.

        Details
        -------

        The call ``np.einsum(einsum_str, x.elem, y.elem, z.elem)`` translates
        into ``x.einsum(einsum_str, y, z)`` for x, y, and z being
        :class:`QteaTorchTensor`.
        """
        tensors = [self.elem] + [tensor.elem for tensor in others]
        elem = to.einsum(einsum_str, *tensors)

        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    # pylint: disable-next=unused-argument
    def fuse_links_update(self, fuse_low, fuse_high, is_link_outgoing=True):
        """
        Fuses one set of links to a single link (inplace-update).

        Parameters
        ----------
        fuse_low : int
            First index to fuse
        fuse_high : int
            Last index to fuse.

        Example: if you want to fuse links 1, 2, and 3, fuse_low=1, fuse_high=3.
        Therefore the function requires links to be already sorted before in the
        correct order.
        """
        self.reshape_update(self._fuse_links_update_shape(fuse_low, fuse_high))

    def get_of(self, variable):
        """Run the get method to transfer to host on variable (same device as self)."""
        if not isinstance(variable, to.Tensor):
            # It is not a to.Tensor, but no other variables can be
            # sent back and forth between CPU and device, so it must
            # be already on the host.
            return variable

        if self.device_str(variable) in ACCELERATOR_DEVICES:
            return variable.detach().to(device=_CPU_DEVICE)

        return variable

    def getsizeof(self):
        """Size in memory (approximate, e.g., without considering meta data)."""
        # Enable fast switch, previously use sys.getsizeof had trouble
        # in resolving size, numpy attribute is only for array without
        # metadata, but metadata like dimensions is only small overhead.
        # (fast switch if we want to use another approach for estimating
        # the size of a numpy array)
        return self._elem.numel() * self._elem.element_size()

    def get_entry(self):
        """Get entry if scalar on host."""
        if np.prod(self.shape) != 1:
            raise QRedTeaError("Cannot use `get_entry`, more than one.")

        if self.device in ACCELERATOR_DEVICES:
            return self._elem.to(device=_CPU_DEVICE).reshape(-1).item()

        return self._elem.reshape(-1).item()

    @classmethod
    # pylint: disable-next=unused-argument
    def mpi_bcast(cls, tensor, comm, tn_mpi_types, tensor_backend, root=0):
        """
        Broadcast QteaTorchTensor via MPI.
        """
        is_root = comm.Get_rank() == root
        dtype = tensor_backend.dtype

        # Broadcast the dim of the shape
        dim = tensor.ndim if is_root else 0
        dim = comm.bcast(dim, root=root)

        # Broadcast shape via numpy
        shape = (
            np.array(list(tensor.shape), dtype=int)
            if is_root
            else np.zeros(dim, dtype=int)
        )
        comm.Bcast([shape, TN_MPI_TYPES["<i8"]], root=root)
        shape = shape.tolist()

        # Broadcast the tensor
        if not is_root:
            obj = cls(shape, ctrl="N", dtype=dtype, device="cpu")
        else:
            obj = tensor

        mpi_type = obj.dtype_mpi()
        # pylint: disable-next=protected-access
        comm.Bcast([obj._elem, mpi_type], root=root)

        obj.convert(device=tensor_backend.memory_device)

        return obj

    # pylint: disable-next=unused-argument
    def mpi_send(self, to_, comm, tn_mpi_types):
        """
        Send tensor via MPI.

        **Arguments**

        to : integer
            MPI process to send tensor to.

        comm : instance of MPI communicator to be used

        tn_mpi_types : dict
            Dictionary mapping dtype to MPI data types.
        """
        mpi_type = self.dtype_mpi()

        # Send the dim of the shape
        comm.send(self.ndim, to_)

        # Send the shape first
        shape = np.array(list(self.shape), dtype=int)
        comm.Send([shape, TN_MPI_TYPES["<i8"]], to_)

        # Send the tensor (trust nvidia support is installed?)
        if self.is_cpu():
            elem = self._elem
        else:
            elem = self._elem.to(device=_CPU_DEVICE)

        comm.Send([elem, mpi_type], to_)

    @classmethod
    # pylint: disable-next=unused-argument
    def mpi_recv(cls, from_, comm, tn_mpi_types, tensor_backend):
        """
        Send tensor via MPI.

        **Arguments**

        from_ : integer
            MPI process to receive tensor from.

        comm : instance of MPI communicator to be used

        tn_mpi_types : dict
            Dictionary mapping dtype to MPI data types.

        tensor_backend : instance of :class:`TensorBackend`
        """
        # Receive the number of legs
        ndim = comm.recv(source=from_)

        # Receive the shape
        shape = np.empty(ndim, dtype=int)
        comm.Recv([shape, TN_MPI_TYPES["<i8"]], from_)
        shape = shape.tolist()

        obj = tensor_backend(shape, ctrl="N", device="cpu", create_base_tensor_cls=True)
        mpi_type = obj.dtype_mpi()

        # Receive the tensor (equivalent to writing _elem)
        # pylint: disable-next=protected-access
        comm.Recv([obj._elem, mpi_type], from_)

        obj.convert(device=tensor_backend.memory_device)

        return obj

    def norm(self):
        """Calculate the norm of the tensor <tensor|tensor>."""
        return self.norm_sqrt() ** 2

    def norm_sqrt(self):
        """
        Calculate the square root of the norm of the tensor,
        i.e., sqrt( <tensor|tensor>).
        """
        if self.is_xla():
            return self._xla_norm_sqrt()
        return to.linalg.vector_norm(self._elem)

    def normalize(self):
        """Normalize tensor with sqrt(<tensor|tensor>)."""
        self._elem /= self.norm_sqrt()

    def remove_dummy_link(self, position):
        """Remove the dummy link at given position (inplace update)."""
        # Could use xp.squeeze
        new_shape = self._remove_dummy_link_shape(position)
        self.reshape_update(new_shape)
        return self

    def scale_link(self, link_weights, link_idx, do_inverse=False):
        """
        Scale tensor along one link at `link_idx` with weights.

        **Arguments**

        link_weights : np.ndarray
            Scalar weights, e.g., singular values.

        link_idx : int
            Link which should be scaled.

        do_inverse : bool, optional
            If `True`, scale with inverse instead of multiplying with
            link weights.
            Default to `False`

        **Returns**

        updated_link : instance of :class:`QteaTensor`
        """
        if do_inverse:
            vec = _scale_link_inverse_vector(link_weights)
            return self.scale_link(vec, link_idx)

        key = self._scale_link_einsum(link_idx)
        tmp = to.einsum(key, self._elem, link_weights)
        return self.from_elem_array(tmp, dtype=self.dtype, device=self.device)

    def scale_link_update(self, link_weights, link_idx, do_inverse=False):
        """
        Scale tensor along one link at `link_idx` with weights (inplace update).

        **Arguments**

        link_weights : np.ndarray
            Scalar weights, e.g., singular values.

        link_idx : int
            Link which should be scaled.

        do_inverse : bool, optional
            If `True`, scale with inverse instead of multiplying with
            link weights.
            Default to `False`
        """
        if do_inverse:
            vec = _scale_link_inverse_vector(link_weights)
            return self.scale_link_update(vec, link_idx)

        if link_idx == 0:
            shape = list(self.shape)
            dim1 = shape[0]
            dim2 = np.prod(shape[1:])
            self.reshape_update((dim1, dim2))

            for ii, scalar in enumerate(link_weights):
                self._elem[ii, :] *= scalar

            self.reshape_update(shape)
            return self

        if link_idx + 1 == self.ndim:
            # For last link xp.multiply will do the job as the
            # last index is one memory block anyway
            self._elem[:] = self._elem * link_weights
            return self

        # Needs permutation, einsum is probably best despite
        # not being tuned to work inplace for now
        key = self._scale_link_einsum(link_idx)
        self._elem = to.einsum(key, self._elem, link_weights)

        return self

    def set_diagonal_entry(self, position, value):
        """Set the diagonal element in a rank-2 tensor (inplace update)"""
        if self.ndim != 2:
            raise QRedTeaRankError("Can only run on rank-2 tensor.")
        self._elem[position, position] = value

    def set_matrix_entry(self, idx_row, idx_col, value):
        """Set one element in a rank-2 tensor (inplace update)"""
        if self.ndim != 2:
            raise QRedTeaRankError("Can only run on rank-2 tensor.")
        self._elem[idx_row, idx_col] = value

    def set_subtensor_entry(self, corner_low, corner_high, tensor):
        """
        Set a subtensor (potentially expensive as looping explicitly, inplace update).

        **Arguments**

        corner_low : list of ints
            The lower index of each dimension of the tensor to set. Length
            must match rank of tensor `self`.

        corner_high : list of ints
            The higher index of each dimension of the tensor to set. Length
            must match rank of tensor `self`.

        tensor : :class:`QteaTorchTensor`
           Tensor to be set as subtensor. Rank must match tensor `self`.
           Dimensions must match `corner_high - corner_low`.

        **Examples**

        To set the tensor of shape 2x2x2 in a larger tensor `self` of shape
        8x8x8 the corresponing call is in comparison to a numpy syntax:

        * self.set_subtensor_entry([2, 4, 2], [4, 6, 4], tensor)
        * self[2:4, 4:6, 2:4] = tensor

        To be able to work with all ranks, we currently avoid the numpy
        syntax in our implementation.
        """
        lists = []
        for ii, corner_ii in enumerate(corner_low):
            corner_jj = corner_high[ii]
            lists.append(list(range(corner_ii, corner_jj)))

        shape = self.elem.shape
        cdim = np.cumprod(np.array(shape[::-1], dtype=int))[::-1]
        cdim = np.array(list(cdim[1:]) + [1], dtype=int)

        # Reshape does not make a copy, but points to memory (unlike flatten)
        self_1d = self.elem.reshape(-1)
        sub_1d = tensor.elem.reshape(-1)

        kk = -1
        for elem in itertools.product(*lists):
            kk += 1
            elem = np.array(elem, dtype=int)
            idx = np.sum(elem * cdim)

            self_1d[idx] = sub_1d[kk]

        # self._elem never changed shape, we are done

    def to_dense(self, true_copy=False):
        """Return dense tensor (if `true_copy=False`, same object may be returned)."""
        if true_copy:
            return self.copy()

        return self

    def to_dense_singvals(self, s_vals, true_copy=False):
        """Convert singular values to dense vector without symmetries."""
        if true_copy:
            return s_vals.detach().clone()

        return s_vals

    def trace(self, return_real_part=False, do_get=False):
        """Take the trace of a rank-2 tensor."""
        if self.ndim != 2:
            raise QRedTeaRankError("Can only run on rank-2 tensor.")

        value = self._elem.trace()

        if return_real_part and value.is_complex():
            value = value.real

        if self.device in ACCELERATOR_DEVICES and do_get:
            value = value.to(device=_CPU_DEVICE)

        return value

    def transpose(self, permutation):
        """Permute the links of the tensor and return new tensor."""
        elem = self._elem.permute(tuple(permutation))
        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def transpose_update(self, permutation):
        """Permute the links of the tensor inplace."""
        self._elem = self._elem.permute(tuple(permutation))

    def write(self, filehandle, cmplx=None):
        """
        Write tensor in original Fortran compatible way.

        **Details**

        1) Number of links
        2) Line with link dimensions
        3) Entries of tensors line-by-line in column-major ordering.
        """
        # Generate numpy version for write
        if self.is_cpu():
            elem_np = self._elem.detach().numpy()
        else:
            elem_np = self._elem.detach().to(device=_CPU_DEVICE).numpy()

        if cmplx is None:
            cmplx = np.sum(np.abs(np.imag(elem_np))) > 1e-15

        write_tensor(elem_np, filehandle, cmplx=cmplx)

    def expm(self, fuse_point=None, prefactor=1):
        """
        Take the matrix exponential with a scalar prefactor, Exp(prefactor * self).
        Reshapes the tensor into a matrix by fusing links up to INCLUDING fuse_point
        into one, and links after into the second dimension.

        Parameters
        ----------
        fuse_point : int, optional
            If given, reshapes the tensor into a matrix by fusing links up to INCLUDING fuse_point
            into one, and links after into the second dimension.
            To compute the exponential of a 4-leg tensor, for example, by fusing (0,1),(2,3),
            set fuse_point=1.
            Default is None.

        prefactor : float, optional
            Prefactor of the tensor to be exponentiated.
            Default to 1.

        Return
        ------
        mat : instance of :class:`QteaTensor`
            Exponential of input tensor.

        Details
        -------

        To compute the exponential of a 4-leg tensor by fusing (0,1),(2,3),
        set fuse_point=1.
        """
        mat = self.copy()
        original_shape = mat.shape

        # Fuse the links.
        if fuse_point is not None:
            mat.fuse_links_update(
                fuse_low=0, fuse_high=fuse_point, is_link_outgoing=False
            )
            mat.fuse_links_update(
                fuse_low=1, fuse_high=mat.ndim - 1, is_link_outgoing=True
            )
        elif mat.ndim != 2:
            raise QRedTeaRankError("Not a matrix, hence cannot take expm.")

        # Take the exponent and reshape back into the original shape.
        # pylint: disable-next=protected-access
        mat._elem = to.matrix_exp(prefactor * mat.elem)
        mat.reshape_update(original_shape)
        return mat

    # --------------------------------------------------------------------------
    #                         Two-tensor operations
    # --------------------------------------------------------------------------

    def add_update(self, other, factor_this=None, factor_other=None):
        """
        Inplace addition as `self = factor_this * self + factor_other * other`.

        **Arguments**

        other : same instance as `self`
            Will be added to `self`. Unmodified on exit.

        factor_this : scalar
            Scalar weight for tensor `self`.

        factor_other : scalar
            Scalar weight for tensor `other`
        """
        if factor_this is not None:
            self._elem *= factor_this

        if factor_other is None:
            factor_other = 1
        elif to.is_tensor(factor_other):
            factor_other = factor_other.item()

        if self.elem.requires_grad or other.elem.requires_grad:
            self._elem = to.add(self._elem, other.elem, alpha=factor_other)
        else:
            to.add(self._elem, other.elem, alpha=factor_other, out=self._elem)

    def dot(self, other):
        """Inner product of two tensors <self|other>."""
        return to.vdot(self.elem.reshape(-1), other.elem.reshape(-1))

    def split_qr(
        self,
        legs_left,
        legs_right,
        perm_left=None,
        perm_right=None,
        is_q_link_outgoing=True,  # pylint: disable=unused-argument
        disable_streams=False,  # pylint: disable=unused-argument
    ):
        """
        Split the tensor via a QR decomposition.

        Parameters
        ----------

        self : instance of :class:`QteaTensor`
            Tensor upon which apply the QR
        legs_left : list of int
            Legs that will compose the rows of the matrix
        legs_right : list of int
            Legs that will compose the columns of the matrix
        perm_left : list of int, optional
            permutations of legs after the QR on left tensor
        perm_right : list of int, optional
            permutation of legs after the QR on right tensor
        disable_streams : boolean, optional
            No effect here, but in general can disable streams
            to avoid nested generation of streams.

        Returns
        -------

        tens_left: instance of :class:`QteaTensor`
            unitary tensor after the QR, i.e., Q.
        tens_right: instance of :class:`QteaTensor`
            upper triangular tensor after the QR, i.e., R
        """
        is_good_bipartition, is_sorted_l, is_sorted_r = self._split_checks_links(
            legs_left, legs_right
        )

        if is_good_bipartition and is_sorted_l and is_sorted_r:
            dim1 = np.prod(np.array(self.shape)[legs_left])
            dim2 = np.prod(np.array(self.shape)[legs_right])

            tens_left, tens_right = self._split_qr_dim(dim1, dim2)

            k_dim = tens_right.shape[0]

            tens_left.reshape_update(list(np.array(self.shape)[legs_left]) + [k_dim])
            tens_right.reshape_update([k_dim] + list(np.array(self.shape)[legs_right]))

        else:
            # Reshaping
            matrix = self._elem.permute(legs_left + legs_right)
            shape_left = np.array(self.shape)[legs_left]
            shape_right = np.array(self.shape)[legs_right]
            matrix = matrix.reshape(np.prod(shape_left), np.prod(shape_right))
            k_dim = np.min([matrix.shape[0], matrix.shape[1]])

            if self.dtype == to.float16:
                matrix = matrix.type(to.float32)

            # QR decomposition
            mat_left, mat_right = to.linalg.qr(matrix)

            if self.dtype == to.float16:
                mat_left = mat_left.to(to.float16)
                mat_right = mat_right.to(to.float16)

            # Reshape back to tensors
            tens_left = self.from_elem_array(
                mat_left.reshape(list(shape_left) + [k_dim]),
                dtype=self.dtype,
                device=self.device,
            )
            tens_right = self.from_elem_array(
                mat_right.reshape([k_dim] + list(shape_right)),
                dtype=self.dtype,
                device=self.device,
            )

        if perm_left is not None:
            tens_left.transpose_update(perm_left)

        if perm_right is not None:
            tens_right.transpose_update(perm_right)

        return tens_left, tens_right

    # pylint: disable-next=unused-argument
    def split_qrte(
        self,
        tens_right,
        singvals_self,
        operator=None,
        conv_params=None,
        is_q_link_outgoing=True,
    ):
        """
        Perform an Truncated ExpandedQR decomposition, generalizing the idea
        of https://arxiv.org/pdf/2212.09782.pdf for a general bond expansion
        given the isometry center of the network on  `tens_left`.
        It should be rather general for three-legs tensors, and thus applicable
        with any tensor network ansatz. Notice that, however, you do not have
        full control on the approximation, since you know only a subset of the
        singular values truncated.

        Parameters
        ----------
        tens_left: xp.array
            Left tensor
        tens_right: xp.array
            Right tensor
        singvals_left: xp.array
            Singular values array insisting on the link to the left of `tens_left`
        operator: xp.array or None
            Operator to contract with the tensors. If None, no operator is contracted

        Returns
        -------
        tens_left: ndarray
            left tensor after the EQR
        tens_right: ndarray
            right tensor after the EQR
        singvals: ndarray
            singular values kept after the EQR
        singvals_cutted: ndarray
            subset of thesingular values cutted after the EQR,
            normalized with the biggest singval
        """
        raise NotImplementedError("QR truncated-expanded not implemented for torch.")

    # torch.linalg has no rq (neither has torch itself)
    # def split_rq(

    # pylint: disable-next=too-many-branches
    def split_svd(
        self,
        legs_left,
        legs_right,
        perm_left=None,
        perm_right=None,
        contract_singvals="N",
        conv_params=None,
        no_truncation=False,
        is_link_outgoing_left=True,  # pylint: disable=unused-argument
        disable_streams=False,  # pylint: disable=unused-argument
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
            No effect here, but in general can disable streams
            to avoid nested generation of streams.

        Returns
        -------
        tens_left: instance of :class:`QteaTensor`
            left tensor after the SVD
        tens_right: instance of :class:`QteaTensor`
            right tensor after the SVD
        singvals: xp.ndarray
            singular values kept after the SVD
        singvals_cut: xp.ndarray
            singular values cut after the SVD, normalized with the biggest singval
        """
        tensor = self._elem

        # Reshaping
        matrix = tensor.permute(legs_left + legs_right)
        shape_left = np.array(tensor.shape)[legs_left]
        shape_right = np.array(tensor.shape)[legs_right]
        matrix = matrix.reshape([np.prod(shape_left), np.prod(shape_right)])

        # Main tensor module does not know about xla - use GPU logic
        device = _GPU_DEVICE if self.device in ACCELERATOR_DEVICES else self.device

        if conv_params is None:
            svd_ctrl = "A"
            max_bond_dimension = min(matrix.shape)
        else:
            svd_ctrl = conv_params.svd_ctrl
            max_bond_dimension = conv_params.max_bond_dimension

        svd_ctrl = _process_svd_ctrl(
            svd_ctrl,
            max_bond_dimension,
            matrix.shape,
            device,
            contract_singvals,
        )
        if matrix.dtype == to.float16:
            matrix = matrix.to(to.float32)

        # SVD decomposition
        if svd_ctrl in ("E", "X"):
            try:
                mat_left, singvals_tot, mat_right = self._split_svd_eigvl(
                    matrix,
                    svd_ctrl,
                    max_bond_dimension,
                    contract_singvals,
                )

            except to._C._LinAlgError:  # pylint: disable=protected-access
                # Likely leads to Cuda memory access error, but let's try
                logger.warning("SVD in mode E or X failed; falling back to mode D.")
                svd_ctrl = "D"

        if svd_ctrl in ("D", "V"):
            try:
                mat_left, singvals_tot, mat_right = self._split_svd_normal(matrix)
            except QRedTeaLinAlgError:
                # Try random SVD instead
                logger.warning("To avoid failure in SVD, switching to random SVD.")
                svd_ctrl = "R"

        if svd_ctrl == "R":
            mat_left, singvals_tot, mat_right = self._split_svd_random(
                matrix, max_bond_dimension
            )

        if self.dtype == to.float16:
            mat_left = mat_left.to(to.float16)
            mat_right = mat_right.to(to.float16)
            singvals_tot = singvals_tot.to(to.float16)

        # Truncation
        if not no_truncation:
            cut, singvals, singvals_cut = self._truncate_singvals(
                singvals_tot, conv_params
            )

            if cut < mat_left.shape[1]:
                # Cutting bond dimension
                mat_left = mat_left[:, :cut]
                mat_right = mat_right[:cut, :]
            elif cut > mat_left.shape[1]:
                # Extending bond dimension to comply with ideal hardware
                # settings
                dim = mat_left.shape[1]
                delta = cut - dim

                mat_left = to.nn.ConstantPad2d((0, delta, 0, 0), 0)(mat_left)
                mat_right = to.nn.ConstantPad2d((0, 0, 0, delta), 0)(mat_right)
                singvals = to.nn.ConstantPad1d((0, delta), 0)(singvals)

        else:
            singvals = singvals_tot
            singvals_cut = []  # xp.array([], dtype=self.dtype)
            cut = mat_left.shape[1]

        # Contract singular values if requested
        if svd_ctrl in ("D", "V", "R"):
            if contract_singvals.upper() == "L":
                mat_left = to.multiply(mat_left, singvals)
            elif contract_singvals.upper() == "R":
                mat_right = to.multiply(singvals, mat_right.T).T
            elif contract_singvals.upper() != "N":
                raise ValueError(
                    f"Contract_singvals option {contract_singvals} is not "
                    + "implemented. Choose between right (R), left (L) or None (N)."
                )

        # Reshape back to tensors
        tens_left = mat_left.reshape(list(shape_left) + [cut])
        if perm_left is not None:
            tens_left = tens_left.permute(perm_left)

        tens_right = mat_right.reshape([cut] + list(shape_right))
        if perm_right is not None:
            tens_right = tens_right.permute(perm_right)

        # Convert into QteaTensor
        tens_left = self.from_elem_array(
            tens_left, dtype=self.dtype, device=self.device
        )
        tens_right = self.from_elem_array(
            tens_right, dtype=self.dtype, device=self.device
        )
        return tens_left, tens_right, singvals, singvals_cut

    def stack_link(self, other, link):
        """
        Stack two tensors along a given link.

        **Arguments**

        other : instance of :class:`QteaTorchTensor`
            Links must match `self` up to the specified link.

        link : integer
            Stack along this link.

        **Returns**

        new_this : instance of :class:QteaTorchTensor`
        """
        newdim_self = list(self.shape)
        newdim_self[link] += other.shape[link]

        dim1, dim2, dim3 = self._shape_as_rank_3(link)
        dim4 = other.shape[link]

        new_dim = dim2 + dim4

        new_this = type(self)(
            [dim1, new_dim, dim3], ctrl="N", dtype=self.dtype, device=self.device
        )
        # pylint: disable-next=protected-access
        new_this._elem[:, :dim2, :] = self._elem.reshape([dim1, dim2, dim3])
        # pylint: disable-next=protected-access
        new_this._elem[:, dim2:, :] = other._elem.reshape([dim1, dim4, dim3])
        new_this.reshape_update(newdim_self)

        return new_this

    # pylint: disable=invalid-name
    def stack_first_and_last_link(self, other):
        """Stack first and last link of tensor targeting MPS addition."""
        newdim_self = list(self.shape)
        newdim_self[0] += other.shape[0]
        newdim_self[-1] += other.shape[-1]

        d1 = self.shape[0]
        d2 = np.prod(self.shape[1:-1])
        d3 = self.shape[-1]
        i1 = other.shape[0]
        i3 = other.shape[-1]

        new_dims = [d1 + i1, d2, d3 + i3]

        new_this = type(self)(new_dims, ctrl="Z", dtype=self.dtype, device=self.device)

        # pylint: disable-next=protected-access
        new_this._elem[:d1, :, :d3] = self.elem.reshape([d1, d2, d3])
        # pylint: disable-next=protected-access
        new_this._elem[d1:, :, d3:] = other.elem.reshape([i1, d2, i3])
        new_this.reshape_update(newdim_self)

        return new_this

    # pylint: disable-next=unused-argument
    def tensordot(self, other, contr_idx, disable_streams=False):
        """Tensor contraction of two tensors along the given indices."""

        # move tensor 'other' to the device of 'self', if needed
        tmp_other_device = other.device
        other.convert(device=self.device)
        if other.device != tmp_other_device:
            logger.warning(
                "Switching tensor device on the fly. (%s -> %s)",
                tmp_other_device,
                other.device,
            )

        elem = to.tensordot(self._elem, other._elem, dims=contr_idx)
        tens = self.from_elem_array(elem, dtype=self.dtype, device=self.device)

        # move 'other' back to original device
        other.convert(device=tmp_other_device)

        return tens

    def stream(self, disable_streams=False):
        """
        Get the instance of a context which can be used to parallelize.

        Parameters
        ----------

        disable_streams : bool, optional
            Allows to disable streams to avoid nested creation of
            streams. Globally, streams should be disabled via the
            `set_streams_qteatorchtensors` function of the corresponding
            base tensor module.
            Default to False.

        Returns
        -------

        Context manager, e.g.,
        :class:`QteaTorchStream` if running on GPU and enabled
        :class:`nullcontext(AbstractContextManager)` otherwise

        """
        if _USE_STREAMS and (not disable_streams) and self.is_gpu():
            return QteaTorchStream()

        return nullcontext()

    @staticmethod
    # pylint: disable-next=unused-argument
    def free_memory_device(device=None):
        """
        Free the unused device memory that is otherwise occupied by the cache.
        Otherwise cupy will keep the memory occupied for caching reasons.
        We follow the approach from https://stackoverflow.com/questions/70508960

        Parameters
        ----------

        device : str | None
            No effect with torch as `to.cuda.empty_cache` does not allow
            to specify a specific device. If enable later via other calls,
            the device is a string, e.g., "gpu:0"
        """
        if GPU_AVAILABLE:
            gc.collect()
            to.cuda.empty_cache()

    # --------------------------------------------------------------------------
    #                       Gradient descent: backwards propagation
    # --------------------------------------------------------------------------

    def get_optimizer(self, *args, **kwargs):
        """Gets the optimizer, e.g. in torch you get the torch.optim.SGD object.

        Parameters
        ----------
        *args: list of tensors to be otimised over

        **kwargs:
        lr: a real number representing the learning rate

        Returns
        ----------
        optimizer: the optimizer object, here torch.optim.SGD
        """
        return to.optim.SGD(*args, **kwargs)

    def backward(self, **kwargs):
        """Implements a step of backward propagation and returns the gradients.

        Parameters
        ----------

        **kwargs:

        retain_graph: boolean, required by PyTorch to retain the graph used to
            calculate the forward function

        Returns
        ----------
        gradients: list of gradients
        """
        if self.ndim != 0:
            raise QRedTeaRankError("Not a scalar, cannot compute gradients")

        return self.elem.backward(**kwargs)

    # --------------------------------------------------------------------------
    #                        Internal methods
    # --------------------------------------------------------------------------
    #
    # inherit _invert_link_selection

    # --------------------------------------------------------------------------
    #                                MISC
    # --------------------------------------------------------------------------

    @staticmethod
    def get_default_datamover():
        """The default datamover compatible with this class."""
        return DataMoverPytorch()

    # --------------------------------------------------------------------------
    #                 Methods needed for _AbstractQteaBaseTensor
    # --------------------------------------------------------------------------

    def assert_diagonal(self, tol=1e-7):
        """Check that tensor is a diagonal matrix up to tolerance."""
        if self.ndim != 2:
            raise QRedTeaRankError("Not a matrix, hence not the identity.")

        tmp = to.diag(to.diag(self._elem))
        tmp -= self._elem

        if to.abs(tmp).max().item() > tol:
            raise QRedTeaError("Matrix not diagonal.")

        return

    def assert_int_values(self, tol=1e-7):
        """Check that there are only integer values in the tensor."""
        if self.is_dtype_complex():
            tmp = to.imag(self.elem)
            if to.abs(tmp).max().item() > tol:
                raise QRedTeaError("Matrix not an integer due to imaginary part.")

            tmp = to.round(to.real(self.elem))
            tmp -= to.real(self.elem)
        else:
            tmp = to.round(self._elem)
            tmp -= self._elem

        if to.abs(tmp).max().item() > tol:
            raise QRedTeaError("Matrix is not an integer matrix.")

        return

    def assert_real_valued(self, tol=1e-7):
        """Check that all tensor entries are real-valued."""
        if not self._elem.is_complex():
            return

        tmp = to.imag(self._elem)

        if to.abs(tmp).max().item() > tol:
            raise QRedTeaError("Tensor is not real-valued.")

    def eig(self):
        """
        Compute eigenvalues and eigenvectors of a two-leg tensor

        Return
        ------
        eigvals, eigvecs : instances of :class:`QteaTorchTensor`
            Eigenvalues and corresponding eigenvectors of input tensor.
        """
        if self.ndim != 2:
            raise QRedTeaRankError("Works only with two-leg tensor")

        eigvals, eigvecs = to.linalg.eig(self.elem)
        eigvals = self.from_elem_array(eigvals, dtype=self.dtype, device=self.device)
        eigvecs = self.from_elem_array(eigvecs, dtype=self.dtype, device=self.device)
        return eigvals, eigvecs

    def elementwise_abs_smaller_than(self, value):
        """Return boolean if each tensor element is smaller than `value`"""
        return (to.abs(self._elem) < value).all().item()

    def _expand_tensor(self, link, new_dim, ctrl="R"):
        """Expand  tensor along given link and to new dimension."""
        newdim = list(self.shape)
        newdim[link] = new_dim - newdim[link]

        expansion = type(self)(newdim, ctrl=ctrl, dtype=self.dtype, device=self.device)

        return self.stack_link(expansion, link)

    def expand_tensor(self, link, new_dim, ctrl="R"):
        """Expand tensor for one link up to dimension `new_dim`."""
        return self._expand_tensor(link, new_dim, ctrl=ctrl)

    def flatten(self):
        """Returns flattened version (rank-1) of dense array in native array type."""
        return self._elem.flatten()

    @classmethod
    def from_elem_array(cls, tensor, dtype=None, device=None):
        """
        New QteaTorchTensor from array

        **Arguments**

        tensor : to.tensor
            Array for new tensor.

        dtype : data type, optional
            Can allow to specify data type.
            If not `None`, it will convert.
            Default to `None`
        """
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global xla_device

        if isinstance(tensor, np.ndarray):
            tensor = to.from_numpy(tensor)

        is_float = tensor.is_complex() or tensor.is_floating_point()
        if dtype is None and (not is_float):
            logger.warning(
                (
                    "Initializing a tensor with integer dtype can be dangerous "
                    "for the simulation. Please specify the dtype keyword in the "
                    "from_elem_array method if it was not intentional."
                )
            )

        if dtype is None:
            dtype = tensor.dtype
        if device is None:
            # We can actually check with torch where we are running
            device = cls.device_str(tensor)

            if cls.is_xla_static(device):
                device = xla_device

        obj = cls(tensor.shape, ctrl=None, dtype=dtype, device=device)
        obj._elem = tensor

        obj.convert(dtype, device)

        return obj

    def get_attr(self, *args):
        """High-risk resolve attribute for an operation on an elementary array."""
        attributes = []

        for elem in args:
            if elem == "cumsum":
                # Special treatment for cumsum to resolve additional argument which
                # is not present in numpy
                attributes.append(_cumsum_like_numpy)
            elif elem == "log":
                # Special treatment to allow integers
                attributes.append(_log_like_numpy)
            elif elem == "sum":
                # Special treatment for cumsum to resolve additional argument which
                # is not present in numpy
                attributes.append(_sum_like_numpy)
            elif not hasattr(to, elem):
                raise QRedTeaError(
                    f"This tensor's elementary array does not support {elem}."
                )
            else:
                attributes.append(getattr(to, elem))

        if len(attributes) == 1:
            return attributes[0]

        return tuple(attributes)

    def get_argsort_func(self):
        """Return callable to argsort function."""
        return to.argsort

    def get_diag_entries_as_int(self):
        """Return diagonal entries of rank-2 tensor as integer on host and as numpy."""
        if self.ndim != 2:
            raise QRedTeaRankError("Not a matrix, cannot get diagonal.")

        tmp = to.diag(self._elem)
        if self.device in ACCELERATOR_DEVICES:
            tmp = tmp.detach().to(device=_CPU_DEVICE)

        if tmp.is_complex():
            tmp = to.real(tmp)

        return tmp.type(to.int32).numpy()

    def get_sqrt_func(self):
        """Return callable to sqrt function."""
        return to.sqrt

    def get_submatrix(self, row_range, col_range):
        """Extract a submatrix of a rank-2 tensor for the given rows / cols."""
        if self.ndim != 2:
            raise QRedTeaRankError("Cannot only set submatrix for rank-2 tensors.")

        row1, row2 = row_range
        col1, col2 = col_range

        return self.from_elem_array(
            self._elem[row1:row2, col1:col2], dtype=self.dtype, device=self.device
        )

    def kron(self, other, idxs=None):
        """
        Perform the kronecker product between two tensors.
        By default, do it over all the legs, but you can also
        specify which legs should be kroned over.
        The legs over which the kron is not done should have
        the same dimension.

        Parameters
        ----------
        other : QteaTensor
            Tensor to kron with self
        idxs : Tuple[int], optional
            Indexes over which to perform the kron.
            If None, kron over all indeces. Default to None.

        Returns
        -------
        QteaTensor
            The kronned tensor

        Details
        -------

        Performing the kronecker product between a tensor of shape (2, 3, 4)
        and a tensor of shape (1, 2, 3) will result in a tensor of shape (2, 6, 12).

        To perform the normal kronecker product between matrices just pass rank-2 tensors.

        To perform kronecker product between vectors first transfor them in rank-2 tensors
        of shape (1, -1)

        Performing the kronecker product only along **some** legs means that along that
        leg it is an elementwise product and not a kronecker. For Example, if idxs=(0, 2)
        for the tensors of shapes (2, 3, 4) and (1, 3, 2) the output will be of shape
        (2, 3, 8).
        """

        subscipts, final_shape = self._einsum_for_kron(self.shape, other.shape, idxs)

        elem = to.einsum(subscipts, self._elem, other._elem).reshape(tuple(final_shape))
        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def mask_to_device(self, mask):
        """
        Send a mask to the device where the tensor is.
        (right now only CPU --> GPU, CPU --> CPU).
        """
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global xla_device

        if self.is_cpu():
            return mask

        if self.is_xla():
            target_device = xla_device
        elif self.is_gpu():
            target_device = self.device
        else:
            raise QRedTeaError(f"Unknown device {self.device}")

        if not to.is_tensor(mask):
            mask = to.from_numpy(np.array(mask, dtype=bool))

        mask_on_device = mask.to(device=target_device)
        return mask_on_device

    def mask_to_host(self, mask):
        """
        Send a mask to the host where we need it for symmetric tensors, e.g.,
        degeneracies. Return as numpy.
        """
        if self.is_cpu():
            if to.is_tensor(mask):
                return mask.numpy()

            return mask

        if to.is_tensor(mask):
            mask_on_host = mask.to(device=_CPU_DEVICE).numpy()
        else:
            mask_on_host = mask

        return mask_on_host

    def permute_rows_cols_update(self, inds):
        """Permute rows and columns of rank-2 tensor with `inds`. Inplace update."""
        if self.ndim != 2:
            raise QRedTeaRankError(
                "Cannot only permute rows & cols for rank-2 tensors."
            )

        tmp = self._elem[inds, :][:, inds]
        self._elem *= 0.0
        self._elem += tmp
        return self

    def prepare_eig_api(self, conv_params):
        """
        Return variables for eigsh.

        **Returns**

        kwargs : dict
            Keyword arguments for eigs call.
            If initial guess can be passed, key "v0" is
            set with value `None`

        LinearOperator : `None`

        eigsh : `None`
        """
        tolerance = conv_params.sim_params["arnoldi_min_tolerance"]

        kwargs = {
            "k": 1,
            "which": "LA",
            "ncv": None,
            "maxiter": None,
            "tol": tolerance,
            "return_eigenvectors": True,
        }

        if self.is_cpu():
            kwargs["v0"] = None

        # For now, we always want to use qtea solver, indicate for
        # symmetric tensors
        kwargs["use_qtea_solver"] = True

        return kwargs, None, None

    def reshape(self, shape, **kwargs):
        """Reshape a tensor."""
        if kwargs.get("order", "C") != "C":
            raise QRedTeaError("Cannot consider order in reshape.")
        elem = self._elem.reshape(shape)
        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def reshape_update(self, shape, **kwargs):
        """Reshape tensor dimensions inplace."""
        if kwargs.get("order", "C") != "C":
            raise QRedTeaError("Cannot consider order in reshape.")
        self._elem = self._elem.reshape(shape)

    def set_submatrix(self, row_range, col_range, tensor):
        """Set a submatrix of a rank-2 tensor for the given rows / cols."""

        if self.ndim != 2:
            raise QRedTeaRankError("Cannot only set submatrix for rank-2 tensors.")

        row1, row2 = row_range
        col1, col2 = col_range

        self._elem[row1:row2, col1:col2] = tensor.elem.reshape(row2 - row1, col2 - col1)

    def subtensor_along_link(self, link, lower, upper):
        """
        Extract and return a subtensor select range (lower, upper) for one line.
        """
        dim1, dim2, dim3 = self._shape_as_rank_3(link)

        elem = self._elem.reshape([dim1, dim2, dim3])
        elem = elem[:, lower:upper, :]

        new_shape = list(self.shape)
        new_shape[link] = upper - lower
        elem = elem.reshape(new_shape)

        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def subtensor_along_link_inds(self, link, inds):
        """
        Extract and return a subtensor via indices for one link.

        Arguments
        ---------

        link : int
            Select only specific indices along this link (but all indices
            along any other link).

        inds : list[int]
            Indices to be selected and stored in the subtensor.

        Returns
        -------

        subtensor : :class:`QteaTorchTensor`
            Subtensor with selected indices.

        Details
        -------

        The numpy equivalent is ``subtensor = tensor[:, :, inds, :]``
        for a rank-4 tensor and ``link=2``.
        """
        # pylint: disable-next=invalid-name
        d1, d2, d3 = self._shape_as_rank_3(link)

        elem = self._elem.reshape([d1, d2, d3])
        elem = elem[:, inds, :]

        new_shape = list(self.shape)
        new_shape[link] = len(inds)
        elem = elem.reshape(new_shape)

        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def _truncate_singvals(self, singvals, conv_params=None):
        """
        Truncate the singular values followling the
        strategy selected in the convergence parameters class

        Parameters
        ----------
        singvals : np.ndarray
            Array of singular values
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use in the procedure. If None is given,
            then use the default convergence parameters of the TN.
            Default to None.

        Returns
        -------
        cut : int
            Number of singular values kept
        singvals_kept : np.ndarray
            Normalized singular values kept
        singvals_cutted : np.ndarray
            Normalized singular values cutted
        """

        if conv_params is None:
            conv_params = TNConvergenceParameters()
            logger.info("Using default convergence parameters.")
        elif not isinstance(conv_params, TNConvergenceParameters):
            raise ValueError(
                "conv_params must be TNConvergenceParameters or None, "
                + f"not {type(conv_params)}."
            )

        if conv_params.trunc_method == "R":
            cut = self._truncate_sv_ratio(singvals, conv_params)
        elif conv_params.trunc_method == "N":
            cut = self._truncate_sv_norm(singvals, conv_params)
        else:
            raise QRedTeaError(f"Unkown trunc_method {conv_params.trunc_method}")

        # Divide singvals in kept and cut (can handle suggested padding)
        singvals_kept = singvals[: min(cut, len(singvals))]
        singvals_cutted = singvals[min(cut, len(singvals)) :]
        # Renormalizing the singular values vector to its norm
        # before the truncation
        norm_kept = (singvals_kept**2).sum()
        norm_trunc = (singvals_cutted**2).sum()
        normalization_factor = to.sqrt(norm_kept / (norm_kept + norm_trunc))
        singvals_kept /= normalization_factor

        # Renormalize cut singular values to track the norm loss
        singvals_cutted /= to.sqrt(norm_trunc + norm_kept)

        return cut, singvals_kept, singvals_cutted

    def _truncate_sv_ratio(self, singvals, conv_params):
        """
        Truncate the singular values based on the ratio
        with the biggest one.

        Parameters
        ----------
        singvals : to.ndarray
            Array of singular values
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use in the procedure.

        Returns
        -------
        cut : int
            Number of singular values kept
        """
        lambda1 = singvals[0]
        cut = to.nonzero(singvals / lambda1 < conv_params.cut_ratio)
        if self.device in ACCELERATOR_DEVICES:
            cut = cut.to(device=_CPU_DEVICE)

        chi_now = len(singvals)
        chi_by_conv = conv_params.max_bond_dimension
        chi_by_ratio = cut[0].item() if len(cut) > 0 else chi_now
        chi_min = conv_params.min_bond_dimension

        return self._truncate_decide_chi(chi_now, chi_by_conv, chi_by_ratio, chi_min)

    def _truncate_sv_norm(self, singvals, conv_params):
        """
        Truncate the singular values based on the
        total norm cut.
        """
        norm = to.cumsum(to.flip(singvals, dims=(0,)), 0)
        norm /= norm[-1].clone()

        # Search for the first index where the constraint is broken,
        # so you need to stop an index before
        cut = to.nonzero(norm > conv_params.cut_ratio)
        if self.is_gpu():
            cut = cut.to(device=_CPU_DEVICE)

        chi_now = len(singvals)
        chi_by_conv = conv_params.max_bond_dimension
        chi_by_norm = len(singvals) - int(cut[0]) if len(cut) > 0 else chi_now
        chi_min = conv_params.min_bond_dimension

        return self._truncate_decide_chi(chi_now, chi_by_conv, chi_by_norm, chi_min)

    def _truncate_decide_chi(self, chi_now, chi_by_conv, chi_by_trunc, chi_min):
        """
        Decide on the bond dimension based on the various values chi and
        potential hardware preference indicated.

        **Arguments**

        chi_now : int
            Current value of the bond dimension

        chi_by_conv : int
            Maximum bond dimension as suggested by convergence parameters.

        chi_by_trunc : int
            Bond dimension suggested by truncating (either ratio or norm).

        chi_min : int
            Minimum bond dimension as suggested by convergence parameters.
        """
        return self._truncate_decide_chi_static(
            chi_now,
            chi_by_conv,
            chi_by_trunc,
            chi_min,
            _BLOCK_SIZE_BOND_DIMENSION,
            _BLOCK_SIZE_BYTE,
            self.elem.element_size(),
        )

    def vector_with_dim_like(self, dim, dtype=None):
        """Generate a vector in the native array of the base tensor."""
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global xla_device

        if dtype is None:
            dtype = self.dtype

        vec = to.empty(dim, dtype=dtype)

        target_device = self.device
        if self.is_gpu(query=target_device):
            vec.to(device="cuda")
        elif self.is_xla(query=target_device):
            vec.to(device=xla_device)

        return vec

    # --------------------------------------------------------------------------
    #             Internal methods (not required by abstract class)
    # --------------------------------------------------------------------------

    @staticmethod
    def device_str(obj):
        """Resolve once the device for qteatorchtensor purposes as str."""
        device_int = obj.get_device()
        device = _CPU_DEVICE if device_int == -1 else f"{_GPU_DEVICE}:{device_int}"
        if device.startswith(_GPU_DEVICE) and XLA_AVAILABLE:
            # Another assumption: if XLA avaivable, it is used
            device = device.replcae(_GPU_DEVICE, _XLA_DEVICE)
        return device

    def dtype_mpi(self):
        """Resolve the dtype for sending tensors via MPI"""
        return {
            # pylint: disable=c-extension-no-member
            "Z": MPI.DOUBLE_COMPLEX,
            "C": MPI.COMPLEX,
            "S": MPI.REAL,
            "D": MPI.DOUBLE_PRECISION,
            "I": MPI.INT,
            # pylint: enable=c-extension-no-member
        }[self.dtype_to_char()]

    # pylint: disable-next=unused-argument
    def _xla_convert(self, dtype, device, stream):
        """Conversion for tensors on XLA (always via host even if on device)."""
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global xla_device

        current = self.device
        do_convert_dtype = (dtype is not None) and (dtype != self.dtype)

        # always convert data types on CPU
        if do_convert_dtype and (not self.is_cpu()):
            self._elem = self._elem.to(device=_CPU_DEVICE)
            current = _CPU_DEVICE

        if do_convert_dtype:
            self._elem = self._elem.type(dtype)

        if device is not None:
            self._convert_check(device)

            if device == current:
                # We already are in the correct device
                pass
            elif self.is_gpu(query=device):
                # We go from the cpu to gpu
                cuda_str = device.replace(_GPU_DEVICE, "cuda")
                self._elem = self._elem.to(device=cuda_str)
            elif self.is_cpu(query=device):
                # We go from gpu to cpu
                self._elem = self._elem.to(device=_CPU_DEVICE)
            elif self.is_xla(query=device):
                # We go from the cpu to xla
                self._elem = self._elem.to(device=xla_device)

        return self

    def _xla_norm_sqrt(self):
        """Avoid problems with complex numbers and vector norm."""
        return to.sqrt(self.dot(self.conj()).real)

    def _split_qr_dim(self, rows, cols):
        """Split via QR knowing dimension of rows and columns."""
        if self.dtype == to.float16:
            matrix = self._elem.type(to.float32).reshape(rows, cols)
            qmat, rmat = to.linalg.qr(matrix)
            qmat = qmat.type(to.float16)
            rmat = rmat.type(to.float16)
        else:
            qmat, rmat = to.linalg.qr(self._elem.reshape(rows, cols))

        qtens = self.from_elem_array(qmat, dtype=self.dtype, device=self.device)
        rtens = self.from_elem_array(rmat, dtype=self.dtype, device=self.device)

        return qtens, rtens

    # pylint: disable-next=unused-argument
    def _split_svd_eigvl(self, matrix, svd_ctrl, max_bond_dimension, contract_singvals):
        """
        SVD of the matrix through an eigvenvalue decomposition.

        Parameters
        ----------
        matrix: to.Tensor
            Matrix to decompose
        svd_crtl : str
            If "E" normal eigenvalue decomposition. If "X" use the sparse.
        max_bond_dimension : int
            Maximum bond dimension
        contract_singvals: str
            Whhere to contract the singular values

        Returns
        -------
        to.Tensor
            Matrix U
        to.Tensor
            Singular values
        to.Tensor
            Matrix V^dagger

        Details
        -------

        We use ᵀ*=^†, the adjoint.

        - In the contract-to-right case, which means:
          H = AAᵀ* = USV Vᵀ*SUᵀ* = U S^2 Uᵀ*
          To compute SVᵀ* we have to use:
          A = USVᵀ* -> Uᵀ* A = S Vᵀ*
        - In the contract-to-left case, which means:
          H = Aᵀ*A = VSUᵀ* USVᵀ* = VS^2 Vᵀ*
          First, we are given V, but we want Vᵀ*. However, let's avoid double work.
          To compute US we have to use:
          A = USVᵀ* -> AV = US
          Vᵀ* = right.T.conj()   (with the conjugation done in place)
        """
        if contract_singvals == "R":
            # The left tensor is unitary
            herm_mat = matrix @ matrix.conj().T
        else:
            # contract_singvals == "L", the right tensor is unitary
            herm_mat = matrix.conj().T @ matrix

        if svd_ctrl == "E":
            eigenvalues, eigenvectors = to.linalg.eigh(herm_mat)
        elif svd_ctrl == "X":
            logger.warning("Falling back from X to E: pytorch has no eigsh.")
            # num_eigvl = min(herm_mat.shape[0] - 1, max_bond_dimension - 1)
            eigenvalues, eigenvectors = to.linalg.eigh(herm_mat)
        else:
            raise ValueError(
                f"svd_ctrl = {svd_ctrl} not valid with eigenvalue decomposition"
            )

        # Eigenvalues are sorted ascendingly, singular values descendengly
        # Only positive eigenvalues makes sense. Due to numerical precision,
        # there will be very small negative eigvl. We put them to 0.
        eigenvalues[eigenvalues < 0] = 0
        singvals = to.sqrt(to.flip(eigenvalues, dims=(0,))[: min(matrix.shape)])
        eigenvectors = to.flip(eigenvectors, dims=(1,))

        # Taking only the meaningful part of the eigenvectors
        if contract_singvals == "R":
            left = eigenvectors[:, : min(matrix.shape)]
            right = left.T.conj() @ matrix
        else:
            right = eigenvectors[:, : min(matrix.shape)]
            left = matrix @ right
            right = to.conj(right.T)

        return left, singvals, right

    def _split_svd_normal(self, matrix):
        """
        Normal SVD of the matrix. First try the faster gesdd iterative method.
        If it fails, resort to gesvd.

        Parameters
        ----------
        matrix: to.Tensor
            Matrix to decompose

        Returns
        -------
        to.Tensor
            Matrix U
        to.Tensor
            Singular values
        to.Tensor
            Matrix V^dagger
        """
        # from torch documentation: By default (driver= None),
        # we call ‘gesvdj’ and, if it fails, we fallback to ‘gesvd’.
        mat_left, singvals_tot, mat_right = to.linalg.svd(matrix, full_matrices=False)

        if self.is_gpu():
            # There is an ugly failure of SVDs on the GPU with inf values without
            # any error message although the matrix is well-behaved (no problem
            # on CPU, can be solved with random SVD on GPU). Go for check over performance
            # here.
            if not to.all(to.isfinite(singvals_tot)):
                raise QRedTeaLinAlgError(
                    "Torch SVD failed with non-finite values for singular values."
                )

        return mat_left, singvals_tot, mat_right

    def _split_svd_random(self, matrix, max_bond_dimension):
        """
        SVD of the matrix through a random SVD decomposition
        as prescribed in page 227 of Halko, Martinsson, Tropp's 2011 SIAM paper:
        "Finding structure with randomness: Probabilistic algorithms for constructing
        approximate matrix decompositions"

        Parameters
        ----------
        matrix: to.Tensor
            Matrix to decompose
        max_bond_dimension : int
            Maximum bond dimension

        Returns
        -------
        to.Tensor
            Matrix U
        to.Tensor
            Singular values
        to.Tensor
            Matrix V^dagger
        """
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global xla_device

        # pylint: disable-next=nested-min-max
        rank = min(max_bond_dimension, min(matrix.shape))

        # This could be parameterized but in the paper they use this
        # value
        n_samples = 2 * rank

        random = to.randn(matrix.shape[1], n_samples, dtype=self.dtype)
        if self.is_gpu():
            random = random.to(device="cuda")
        elif self.is_xla():
            random = random.to(device=xla_device)

        reduced_matrix = matrix @ random
        # Find orthonormal basis
        ortho, _ = to.linalg.qr(reduced_matrix)

        # Second part
        to_svd = ortho.T @ matrix
        left_tilde, singvals, right = to.linalg.svd(to_svd, full_matrices=False)
        left = ortho @ left_tilde

        return left, singvals, right


def _scale_link_inverse_vector(link_weights):
    """Construct the inverse of singular values setting zeros to one."""
    # Have to handle zeros here ... as we allow padding singular
    # values with zeros, we must also automatically avoid division
    # by zero due to exact zeros. But we can assume it must be at
    # the end of the array
    vec = to.clone(link_weights)
    if link_weights[-1] == 0.0:
        vec[vec == 0.0] = 1.0

    vec = 1.0 / vec
    return vec


def _cumsum_like_numpy(array, axis=None, **kwargs):
    """Provide cumsum function with same arguments as numpy."""
    # numpy has default of axis=None which acts on the flattened array
    # which torch does not support
    if axis is None and array.ndim != 1:
        raise QRedTeaRankError("Running cumsum without axis on tensor with rank != 1.")

    if axis is None:
        axis = 0

    return to.cumsum(array, axis, **kwargs)


def _log_like_numpy(array):
    """Provide log function accepting as well scalar integers not being a tensor."""
    if isinstance(array, to.Tensor):
        return to.log(array)

    return math.log(array)


def _sum_like_numpy(array, axis=None, **kwargs):
    """Provide sum function with same arguments as numpy."""
    # numpy has default of axis=None which acts on the flattened array
    # which torch does not support
    if axis is None:
        return to.sum(array, **kwargs)

    return to.sum(array, axis, **kwargs)


class DataMoverPytorch(_AbstractDataMover):
    """
    Data mover to move QteaTorchTensor between torch CPU and torch GPU format.
    """

    tensor_cls = (QteaTorchTensor,)

    def __init__(self):
        pass

    @property
    def device_memory(self):
        """Current memory occupied in the device"""
        # return self.mempool.used_bytes()
        raise NotImplementedError("pytorch data mover")

    def sync_move(self, tensor, device):
        """
        Move the tensor `tensor` to the device `device`
        synchronously with the main computational stream

        Parameters
        ----------
        tensor : _AbstractTensor
            The tensor to be moved
        device: str
            The device where to move the tensor
        """
        if GPU_AVAILABLE or XLA_AVAILABLE:
            tensor.convert(dtype=None, device=device)

    # pylint: disable-next=unused-argument
    def async_move(self, tensor, device, stream=None):
        """
        Move the tensor `tensor` to the device `device`
        asynchronously with respect to the main computational
        stream

        Parameters
        ----------
        tensor : _AbstractTensor
            The tensor to be moved
        device: str
            The device where to move the tensor
        stream : stream-object
            Stream to be used to move the data if a stream
            different from the data mover's stream should be
            used.
            Default to None (use DataMover's stream)
        """
        logger.debug("Moving still sync for pytorch.")
        self.sync_move(tensor, device)

    def wait(self):
        """
        Put a barrier for the streams and wait them
        """
        # pylint: disable-next=unnecessary-pass
        pass


def default_pytorch_backend(device="cpu", dtype=to.complex128):
    """
    Generate a default tensor backend for dense tensors, i.e., with
    a :class:`QteaTorchTensor`.

    **Arguments**

    dtype : data type, optional
        Data type for pytorch.
        Default to to.complex128

    device : device specification, optional
        Default to `"cpu"`.
        Available: `"cpu", "gpu", "xla"`

    **Returns**

    tensor_backend : :class:`TensorBackend`
    """
    tensor_backend = TensorBackend(
        tensor_cls=QteaTorchTensor,
        base_tensor_cls=QteaTorchTensor,
        device=device,
        dtype=dtype,
        symmetry_injector=None,
        datamover=DataMoverPytorch(),
    )

    return tensor_backend


def default_abelian_pytorch_backend(device="cpu", dtype=to.complex128):
    """
    Generate a default tensor backend for symmetric tensors, i.e., with
    a :class:`QteaTorchTensor`. The tensors support Abelian symmetries.

    **Arguments**

    dtype : data type, optional
        Data type for pytorch.
        Default to to.complex128

    device : device specification, optional
        Default to `"cpu"`.
        Available: `"cpu", "gpu", "xla"`

    **Returns**

    tensor_backend : :class:`TensorBackend`
    """
    tensor_backend = TensorBackend(
        tensor_cls=QteaAbelianTensor,
        base_tensor_cls=QteaTorchTensor,
        device=device,
        dtype=dtype,
        symmetry_injector=AbelianSymmetryInjector(),
        datamover=DataMoverPytorch(),
    )

    return tensor_backend
