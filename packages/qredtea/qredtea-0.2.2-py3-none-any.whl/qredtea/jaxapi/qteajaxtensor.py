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
Tensor class based on JAX; JAX supports both CPU and GPU in one framework.
"""

# pylint: disable=too-many-branches
# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-many-arguments
# pylint: disable=too-many-public-methods
# pylint: disable=wrong-import-position

import itertools
import os
from contextlib import nullcontext
from warnings import warn

import numpy as np

# pylint: disable-next=wrong-import-order,ungrouped-imports
from qredtea.tooling import QRedTeaBackendLibraryImportError

try:
    import jax
    import jax.numpy as jnp
    import jaxlib
except ImportError as exc:
    raise QRedTeaBackendLibraryImportError() from exc

# pylint: disable=import-error, no-name-in-module
from qtealeaves.convergence_parameters import TNConvergenceParameters
from qtealeaves.operators import TNOperators
from qtealeaves.solvers import EigenSolverH
from qtealeaves.tensors import (
    QteaTensor,
    TensorBackend,
    _AbstractDataMover,
    _AbstractQteaBaseTensor,
    _process_svd_ctrl,
)
from qtealeaves.tooling import write_tensor
from qtealeaves.tooling.devices import _CPU_DEVICE, _GPU_DEVICE, _XLA_DEVICE, DeviceList

from qredtea.symmetries import AbelianSymmetryInjector, QteaAbelianTensor
from qredtea.tooling import (
    QRedTeaDataTypeError,
    QRedTeaDeviceError,
    QRedTeaError,
    QRedTeaLinkError,
    QRedTeaRankError,
)

# pylint: enable=import-error, no-name-in-module

# pylint: disable-next=invalid-name
cpu_device = jax.devices("cpu")[0]

ACCELERATOR_DEVICES = DeviceList([_GPU_DEVICE, _XLA_DEVICE])

try:
    gpu_device_list = jax.devices("gpu")
    GPU_AVAILABLE = True
    # pylint: disable-next=invalid-name
    gpu_device = gpu_device_list[0]
except RuntimeError:
    GPU_AVAILABLE = False
    # pylint: disable-next=invalid-name
    gpu_device = None

try:
    tpu_device_list = jax.devices("tpu")
    XLA_AVAILABLE = True
    # pylint: disable-next=invalid-name
    xla_device = tpu_device_list[0]
except RuntimeError:
    XLA_AVAILABLE = False
    # pylint: disable-next=invalid-name
    xla_device = None

# Jax needs always key for random number generator (not thread-safe if
# used in threaded simulations)
# pylint: disable-next=invalid-name
key_rng = jax.random.key(0)


# pylint: disable-next=invalid-name
_BLOCK_SIZE_BOND_DIMENSION = os.environ.get("QTEA_BLOCK_SIZE_BOND_DIMENSION", None)
# pylint: disable-next=invalid-name
_BLOCK_SIZE_BYTE = os.environ.get("QTEA_BLOCK_SIZE_BYTE", None)

if _BLOCK_SIZE_BOND_DIMENSION is not None:
    _BLOCK_SIZE_BOND_DIMENSION = int(_BLOCK_SIZE_BOND_DIMENSION)
if _BLOCK_SIZE_BYTE is not None:
    _BLOCK_SIZE_BYTE = int(_BLOCK_SIZE_BYTE)

__all__ = [
    "QteaJaxTensor",
    "default_jax_backend",
    "default_abelian_jax_backend",
    "set_block_size_qteajaxtensors",
    "DataMoverJax",
]


def set_block_size_qteajaxtensors(block_size_bond_dimension=None, block_size_byte=None):
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
        warn("Ignoring BLOCK_SIZE_BOND_DIMENSION in favor of BLOCK_SIZE_BYTE.")


# class set_block_size_qteajaxtensors once to resolve if both variables
# are set
set_block_size_qteajaxtensors(_BLOCK_SIZE_BOND_DIMENSION, _BLOCK_SIZE_BYTE)


class QteaJaxTensor(_AbstractQteaBaseTensor):
    """
    Tensor for Quantum TEA based on JAX tensors.
    """

    implemented_devices = ("cpu", "gpu", "xla")

    def __init__(
        self,
        links,
        ctrl="Z",
        are_links_outgoing=None,  # pylint: disable=unused-argument
        base_tensor_cls=None,  # pylint: disable=unused-argument
        dtype=jnp.complex64,
        device=None,
        requires_grad=None,
    ):
        """

        links : list of ints with shape (links works towards generalization)
        """
        # pylint: disable-next=invalid-name,global-statement
        global key_rng

        super().__init__(links)

        if requires_grad is not None:
            raise ValueError("Autograd not supported")
        if ctrl is None:
            self._elem = None
            return

        if ctrl in ["N"]:
            # Is there just something uninitialized?
            self._elem = jnp.zeros(links, dtype=dtype)
        elif ctrl in ["O"]:
            self._elem = jnp.ones(links, dtype=dtype)
        elif ctrl in ["Z"]:
            self._elem = jnp.zeros(links, dtype=dtype)
        elif ctrl in ["1", "eye"]:
            if len(links) != 2:
                raise ValueError("Initialization with identity only for rank-2.")
            if links[0] != links[1]:
                raise ValueError("Initialization with identity only for square matrix.")
            self._elem = jnp.eye(links[0], dtype=dtype)
        elif ctrl in ["R", "random"]:
            if dtype in [jnp.complex64, jnp.complex128]:
                key_rng, subkey_r = jax.random.split(key_rng)
                key_rng, subkey_c = jax.random.split(key_rng)
                tmp_r = jax.random.uniform(subkey_r, shape=links, dtype=jnp.float32)
                tmp_c = (
                    jax.random.uniform(subkey_c, shape=links, dtype=jnp.float32) * 1j
                )
                self._elem = tmp_r + tmp_c
            else:
                key_rng, subkey_r = jax.random.split(key_rng)
                self._elem = jax.random.uniform(subkey_r, shape=links, dtype=dtype)
        elif ctrl in ["ground"]:
            dim = int(np.prod(links))
            tmp = jnp.zeros([dim], dtype=dtype)
            tmp = tmp.at[0].set(1)
            self._elem = jnp.reshape(tmp, links)
        elif np.isscalar(ctrl) and np.isreal(ctrl):
            # This prohibits initialization with complex numbers.
            # In case of adding complex numbers, enforce a complex dtype!
            self._elem = ctrl * jnp.ones(links, dtype=dtype)
        else:
            raise QRedTeaError(f"Unknown initialization {ctrl}.")

        self.convert(dtype, device)

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
            "float16": 1e-3,
            "float32": 1e-7,
            "float64": 1e-14,
            "complex64": 1e-7,
            "complex128": 1e-14,
        }

        return eps_dict[str(self.dtype)]

    @property
    def linear_algebra_library(self):
        """Specification of the linear algebra library used as string `jax``."""
        return "jax"

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
        new_tensor = QteaJaxTensor(self.links, ctrl=None)
        if isinstance(other, QteaJaxTensor):
            new_tensor._elem = jnp.add(self.elem, other.elem)
        else:
            # Assume it is scalar then
            new_tensor._elem = jnp.add(self.elem, other)

        return new_tensor

    def __iadd__(self, other):
        """In-place addition of tensor with tensor or scalar (update)."""
        if isinstance(other, QteaJaxTensor):
            self._elem = jnp.add(self.elem, other.elem)
        else:
            # Assume it is scalar then
            self._elem = jnp.add(self.elem, other)

        return self

    def __mul__(self, factor):
        """Multiplication of tensor with scalar returning new tensor as result."""
        if isinstance(factor, jnp.ndarray):
            tmp = factor * self._elem
        else:
            tmp = jnp.asarray(factor, dtype=self.elem.dtype) * self._elem
        return QteaJaxTensor.from_elem_array(tmp, dtype=self.dtype, device=self.device)

    def __matmul__(self, other):
        """Matrix multiplication as contraction over last and first index of self and other."""
        idx = self.ndim - 1
        return self.tensordot(other, ([idx], [0]))

    def __imul__(self, factor):
        """In-place multiplication of tensor with scalar (update)."""
        if isinstance(factor, jnp.ndarray):
            self._elem = factor * self.elem
        else:
            self._elem = jnp.asarray(factor, dtype=self.elem.dtype) * self.elem
        return self

    def __itruediv__(self, factor):
        """In-place division of tensor with scalar (update)."""
        if factor == 0:
            raise ZeroDivisionError("Trying to divide by zero.")
        if isinstance(factor, jnp.ndarray):
            self._elem /= factor
        else:
            # On GPU, tracked cases converting data type during division
            # when called with numpy data type (float64) from eigensolver
            self._elem /= jnp.asarray(factor, dtype=self.dtype)
        return self

    def __sub__(self, other):
        """
        Subtraction of a scalar to a tensor adds it to all the entries.
        If other is another tensor, elementwise subtraction if they have the same shape
        """
        new_tensor = QteaJaxTensor(self.links, ctrl=None)
        if isinstance(other, QteaJaxTensor):
            new_tensor._elem = jnp.subtract(self.elem, other.elem)
        else:
            # Assume it is scalar then
            new_tensor._elem = jnp.subtract(self.elem, other)

        return new_tensor

    def __truediv__(self, factor):
        """Division of tensor with scalar."""
        if factor == 0:
            raise ZeroDivisionError("Trying to divide by zero.")
        elem = self._elem / factor
        return QteaJaxTensor.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def __neg__(self):
        """Negative of a tensor returned as a new tensor."""
        # pylint: disable-next=invalid-unary-operand-type
        neg_elem = -self._elem
        return QteaJaxTensor.from_elem_array(
            neg_elem, dtype=self.dtype, device=self.device
        )

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
        dtype=jnp.complex64,
        device="cpu",
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
            Default to `jnp.complex64`

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
        dtype_numpy = QteaJaxTensor.dtype_to_numpy(dtype)

        qteatensor_dict = QteaTensor.convert_operator_dict(
            op_dict,
            params=params,
            symmetries=symmetries,
            generators=generators,
            base_tensor_cls=base_tensor_cls,
            dtype=dtype_numpy,
            device=_CPU_DEVICE,
        )

        new_op_dict = TNOperators(
            set_names=qteatensor_dict.set_names,
            mapping_func=qteatensor_dict.mapping_func,
        )
        for key, value in qteatensor_dict.items():
            new_op_dict[key] = QteaJaxTensor.from_qteatensor(value)
            new_op_dict[key].convert(dtype, device)

        return new_op_dict

    def copy(self, dtype=None, device=None):
        """Make a copy of a tensor; using detach and clone."""
        if dtype is None:
            dtype = self.dtype
        if device is None:
            device = self.device
        return self.from_elem_array(self._elem.copy(), dtype=dtype, device=device)

    def eye_like(self, link):
        """
        Generate identity matrix.

        **Arguments**

        self : instance of :class:`QteaTensor`
            Extract data type etc from this one here.

        link : same as returned by `links` property, here integer.
            Dimension of the square, identity matrix.
        """
        elem = jnp.eye(link)
        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    @classmethod
    def from_qteatensor(cls, qteatensor, dtype=None, device=None):
        """Convert QteaTensor based on numpy/cupy into QteaJaxTensor."""
        elem = jnp.asarray(qteatensor.elem)
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
        # pylint: disable-next=invalid-name,global-statement
        global key_rng

        key_rng, subkey = jax.random.split(key_rng)
        elem = jax.random.uniform(subkey, shape=[link, link])
        elem, _ = jnp.linalg.qr(elem)

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
        """Return a dummy link based on an example."""
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

    def zeros_like(self):
        """Get a tensor same as `self` but filled with zeros."""
        return QteaJaxTensor(self.shape, ctrl="Z", dtype=self.dtype, device=self.device)

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

        return jnp.isclose(self.elem, other.elem, atol=tol).all()

    def assert_identical_irrep(self, link_idx):
        """Assert that specified link is identical irreps."""
        if self.shape[link_idx] != 1:
            raise QRedTeaLinkError("Link dim is greater one in identical irrep check.")

    def assert_identity(self, tol=1e-7):
        """Check if tensor is an identity matrix."""

        if not self.is_close_identity(tol=tol):
            print("Error information tensor", self._elem)
            raise QRedTeaError("Tensor not diagonal with ones.")

    def is_close_identity(self, tol=1e-7):
        """Check if rank-2 tensor is close to identity."""
        if self.ndim != 2:
            return False

        if self.shape[0] != self.shape[1]:
            return False

        eye = jnp.eye(self.shape[0])

        eps = float(jnp.max(jnp.abs(self.elem - eye)))

        return eps < tol

    def is_dtype_complex(self):
        """Check if data type is complex."""
        return jnp.issubdtype(self._elem.dtype, jnp.complexfloating)

    @staticmethod
    def is_cpu_static(device_str):
        """
        Check if device is CPU or not.

        Parameters
        ----------

        device_str : str
            Check for this string if it corresponds to a CPU.

        Returns
        -------

        is_cpu : bool
            True if device is a CPU.
        """
        # Later we can enable idx in GPU
        # return device_str.startswith(_CPU_DEVICE)
        return device_str == _CPU_DEVICE

    @staticmethod
    def is_gpu_static(device_str):
        """
        Check if device is GPU or not.

        Parameters
        ----------

        device_str : str
            Check for this string if it is a GPU device.

        Returns
        -------

        is_gpu : bool
            True if device is a GPU.
        """
        # Later we can enable idx in GPU
        # return device_str.startswith(_GPU_DEVICE)
        return device_str == _GPU_DEVICE

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
        return (
            self.is_cpu_static(query)
            or self.is_gpu_static(query)
            or self.is_xla_static(query)
        )

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
        # Later we can enable idx in GPU
        # return device_str.startswith(_XLA_DEVICE)
        return device_str == _XLA_DEVICE

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
        return QteaJaxTensor.from_elem_array(
            self._elem.conj(), dtype=self.dtype, device=self.device
        )

    def conj_update(self):
        """Apply the complex conjugated to the tensor in place."""
        self._elem = self.elem.conj()

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
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global cpu_device, gpu_device, xla_device

        # Both devices available, figure out what we currently have
        # and start converting
        current = self.device

        if device is not None:
            self._convert_check(device)

            if device == current:
                # We already are in the correct device
                pass
            elif self.is_gpu(query=device):
                # We go from the cpu to gpu
                self._elem = jax.device_put(self.elem, device=gpu_device)
            elif self.is_cpu(query=device):
                # We go from gpu to cpu
                self._elem = jax.device_put(self.elem, device=cpu_device)
            elif self.is_xla(query=device):
                # There seems to be only the option to go
                # via "with" for conversion
                self._elem = jax.device_put(self.elem, device=xla_device)
            else:
                raise QRedTeaDeviceError(
                    "Conversion not possible or not considered yet."
                )

        if (dtype is not None) and (dtype != self.dtype):
            self._elem = self._elem.astype(dtype=dtype)

        return self

    def convert_singvals(self, singvals, dtype, device):
        """Convert the singular values via a tensor."""
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global cpu_device, gpu_device, xla_device

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
                singvals = jax.device_put(singvals, device=gpu_device)
            elif self.is_cpu(query=device):
                # We go from gpu to cpu
                singvals = jax.device_put(singvals, device=cpu_device)
            elif self.is_xla(query=device):
                # We go from the cpu to xla
                singvals = jax.device_put(singvals, device=xla_device)

        if dtype is not None:
            if dtype != singvals.dtype:
                singvals = singvals.astype(dtype=dtype)

        return singvals

    def diag(self, real_part_only=False, do_get=False):
        """Return the diagonal as array of rank-2 tensor."""
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global cpu_device

        if self.ndim != 2:
            raise QRedTeaRankError("Can only run on rank-2.")

        diag = jnp.diag(self.elem)

        if real_part_only:
            diag = jnp.real(diag)

        if self.device in ACCELERATOR_DEVICES and do_get:
            diag = jax.device_put(diag, device=cpu_device)

        return diag

    def dtype_from_char(self, dtype):
        """Resolve data type from chars C, D, S, Z and optionally H."""
        data_types = {
            "A": jnp.complex128,
            "C": jnp.complex64,
            "D": jnp.float64,
            "H": jnp.float16,
            "S": jnp.float32,
            "Z": jnp.complex128,
            "I": jnp.int32,
        }

        jax_dtype = data_types[dtype]

        # Double check was enabled ... data types can be available
        # depending on device and environment variable set as
        # `export JAX_ENABLE_X64=True`
        # if dtype in ["A", "C", "Z"]:
        #    tmp = jnp.ones([1], dtype=jax_dtype)
        #    if tmp.dtype != jax_dtype:
        #        raise QRedTeaError(f"Data type `{dtype}` not provided by JAX.")

        return jax_dtype

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
        eig_api_qtea_half = self.dtype == jnp.float16

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
        injected_funcs = {
            "abs": jnp.abs,
        }

        solver = EigenSolverH(
            self,
            matvec_func,
            conv_params,
            args_func=args_func,
            kwargs_func=kwargs_func,
            injected_funcs=injected_funcs,
        )

        return solver.solve()

    def eig_api_arpack(
        self, matvec_func, links, conv_params, args_func=None, kwargs_func=None
    ):
        """
        Interface to hermitian eigenproblem via Arpack.
        """
        raise NotImplementedError("Arpack is non-default interface for JAX.")

    def einsum(self, einsum_str, *others):
        """
        Call to einsum with `self` as first tensor.

        Arguments
        ---------

        einsum_str : str
            Einsum contraction rule.

        other: List[:class:`QteaJaxTensors`]
            2nd, 3rd, ..., n-th tensor in einsum rule as
            positional arguments.

        Results
        -------

        tensor : :class:`QteaJaxTensor`
            Contracted tensor according to the einsum rules.

        Details
        -------

        The call ``np.einsum(einsum_str, x.elem, y.elem, z.elem)`` translates
        into ``x.einsum(einsum_str, y, z)`` for x, y, and z being
        :class:`QteaJaxTensor`.
        """
        # List of :class:`AbstractQteaTensors
        tensors = [self] + list(others)

        # Jax has by default optimize='Optimal', we do not mess with this here
        # Convert to actual data type of backend
        tensors = [tensor.elem for tensor in tensors]

        elem = jnp.einsum(einsum_str, *tensors)

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
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global cpu_device

        # pylint: disable-next=c-extension-no-member,isinstance-second-argument-not-valid-type
        if not isinstance(variable, jaxlib.xla_extension.ArrayImpl):
            # It is not a jax array, but no other variables can be
            # sent back and forth between CPU and device, so it must
            # be already on the host.
            return variable

        if self.device_str(variable) in ACCELERATOR_DEVICES:
            return jax.device_put(variable, device=cpu_device)

        return variable

    def getsizeof(self):
        """Size in memory (approximate, e.g., without considering meta data)."""
        # Enable fast switch, previously use sys.getsizeof had trouble
        # in resolving size, numpy attribute is only for array without
        # metadata, but metadata like dimensions is only small overhead.
        # (fast switch if we want to use another approach for estimating
        # the size of a numpy array)
        return self._elem.nbytes

    def get_entry(self):
        """Get entry if scalar on host."""
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global cpu_device

        if np.prod(self.shape) != 1:
            raise QRedTeaError("Cannot use `get_entry`, more than one.")

        if self.device in ACCELERATOR_DEVICES:
            return np.asarray(jax.device_put(self.elem, device=cpu_device)).flatten()[0]

        return np.asarray(self._elem).flatten()[0]

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
        raise NotImplementedError("QteaJaxTensor has no MPI support yet.")

    @classmethod
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
        raise NotImplementedError("QteaJaxTensor has no MPI support yet.")

    def norm(self):
        """Calculate the norm of the tensor <tensor|tensor>."""
        return self.norm_sqrt() ** 2

    def norm_sqrt(self):
        """
        Calculate the square root of the norm of the tensor,
        i.e., sqrt( <tensor|tensor>).
        """
        return jnp.linalg.norm(self.elem)

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

        updated_link : instance of :class:`QteaJaxTensor`

        **Details**

        The inverse implementation handles zeros correctly which
        have been introduced due to padding. Therefore, `scale_link`
        should be used over passing `1 / link_weights` to this function.
        """
        key = self._scale_link_einsum(link_idx)

        if do_inverse:
            vec = _scale_link_inverse_vector(link_weights)
            tmp = jnp.einsum(key, self._elem, vec)

        else:
            # Non inverse, just regular contraction
            tmp = jnp.einsum(key, self._elem, link_weights)

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

        **Details**

        The inverse implementation handles zeros correctly which
        have been introduced due to padding. Therefore, `scale_link`
        should be used over passing `1 / link_weights` to this function.
        """
        if do_inverse:
            vec = _scale_link_inverse_vector(link_weights)
        else:
            vec = link_weights

        if link_idx == 0:
            key = self._scale_link_einsum(link_idx)
            self._elem = jnp.einsum(key, self._elem, vec)
            return self

        if link_idx + 1 == self.ndim:
            # For last link xp.multiply will do the job as the
            # last index is one memory block anyway
            self._elem = jnp.multiply(self._elem, vec)
            return self

        # Need permutation or einsum, prefer einsum
        key = self._scale_link_einsum(link_idx)
        self._elem = jnp.einsum(key, self._elem, vec)
        return self

    def set_diagonal_entry(self, position, value):
        """Set the diagonal element in a rank-2 tensor (inplace update)"""
        if self.ndim != 2:
            raise QRedTeaRankError("Can only run on rank-2 tensor.")
        self._elem = self.elem.at[position, position].set(value)

    def set_matrix_entry(self, idx_row, idx_col, value):
        """Set one element in a rank-2 tensor (inplace update)"""
        if self.ndim != 2:
            raise QRedTeaRankError("Can only run on rank-2 tensor.")
        self._elem = self.elem.at[idx_row, idx_col].set(value)

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

        tensor : :class:`QteaJaxTensor`
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

            self_1d = self_1d.at[idx].set(sub_1d[kk])

        self._elem = self_1d.reshape(shape)

    def to_dense(self, true_copy=False):
        """Return dense tensor (if `true_copy=False`, same object may be returned)."""
        if true_copy:
            return self.copy()

        return self

    def to_dense_singvals(self, s_vals, true_copy=False):
        """Convert singular values to dense vector without symmetries."""
        if true_copy:
            return s_vals.copy()

        return s_vals

    def trace(self, return_real_part=False, do_get=False):
        """Take the trace of a rank-2 tensor."""
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global cpu_device

        if self.ndim != 2:
            raise QRedTeaRankError("Can only run on rank-2 tensor.")

        value = jnp.trace(self._elem)

        if return_real_part and self.is_dtype_complex():
            value = jnp.real(value)

        if self.device in ACCELERATOR_DEVICES and do_get:
            value = jax.device_put(value, device=cpu_device)

        return value

    def transpose(self, permutation):
        """Permute the links of the tensor and return new tensor."""
        tens = QteaJaxTensor(None, ctrl=None, dtype=self.dtype, device=self.device)
        # pylint: disable-next=protected-access
        tens._elem = jnp.transpose(self._elem, permutation)
        return tens

    def transpose_update(self, permutation):
        """Permute the links of the tensor inplace."""
        self._elem = jnp.transpose(self._elem, tuple(permutation))

    def write(self, filehandle, cmplx=None):
        """
        Write tensor in original Fortran compatible way.

        **Details**

        1) Number of links
        2) Line with link dimensions
        3) Entries of tensors line-by-line in column-major ordering.
        """
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global cpu_device

        # Generate numpy version for write
        if self.is_cpu():
            elem_np = np.asarray(self._elem)
        else:
            tmp = jax.device_put(self.elem, device=cpu_device)
            elem_np = np.asarray(tmp)

        if cmplx is None:
            cmplx = np.sum(np.abs(np.imag(elem_np))) > 1e-15

        write_tensor(elem_np, filehandle, cmplx=cmplx)

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
            self._elem = jnp.add(self.elem, other.elem)
        elif isinstance(factor_other, jnp.ndarray):
            self._elem = jnp.add(self.elem, factor_other * other.elem)
        else:
            factor_other = jnp.asarray(factor_other, dtype=other.elem.dtype)
            self._elem = jnp.add(self.elem, factor_other * other.elem)

    def dot(self, other):
        """Inner product of two tensors <self|other>."""
        return jnp.vdot(self.elem, other.elem)

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
            matrix = jnp.transpose(self._elem, legs_left + legs_right)
            shape_left = np.array(self.shape)[legs_left]
            shape_right = np.array(self.shape)[legs_right]
            matrix = jnp.reshape(matrix, [np.prod(shape_left), np.prod(shape_right)])
            k_dim = np.min([matrix.shape[0], matrix.shape[1]])

            if (self.dtype == jnp.float16) and self.is_cpu():
                matrix = matrix.astype(jnp.float32)

            # QR decomposition
            mat_left, mat_right = jnp.linalg.qr(matrix)

            if (self.dtype == jnp.float16) and self.is_cpu():
                mat_left = mat_left.astype(jnp.float16)
                mat_right = mat_right.astype(jnp.float16)

            # Reshape back to tensors
            tens_left = self.from_elem_array(
                jnp.reshape(mat_left, list(shape_left) + [k_dim]),
                dtype=self.dtype,
                device=self.device,
            )
            tens_right = self.from_elem_array(
                jnp.reshape(mat_right, [k_dim] + list(shape_right)),
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
        raise NotImplementedError("QR truncated-expanded not implemented for JAX.")

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
        matrix = jnp.transpose(tensor, legs_left + legs_right)
        shape_left = np.array(tensor.shape)[legs_left]
        shape_right = np.array(tensor.shape)[legs_right]
        matrix = jnp.reshape(matrix, [np.prod(shape_left), np.prod(shape_right)])

        # Main tensor module does not know about xla - use GPU logic
        device = "gpu" if self.device in ACCELERATOR_DEVICES else self.device

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
        if (matrix.dtype == jnp.float16) and self.is_cpu():
            matrix = matrix.astype(jnp.float32)

        # SVD decomposition
        if svd_ctrl in ("D", "V"):
            mat_left, singvals_tot, mat_right = self._split_svd_normal(matrix)
        elif svd_ctrl in ("E", "X"):
            mat_left, singvals_tot, mat_right = self._split_svd_eigvl(
                matrix,
                svd_ctrl,
                max_bond_dimension,
                contract_singvals,
            )
        elif svd_ctrl == "R":
            mat_left, singvals_tot, mat_right = self._split_svd_random(
                matrix, max_bond_dimension
            )

        if (self.dtype == jnp.float16) and self.is_cpu():
            mat_left = mat_left.astype(jnp.float16)
            mat_right = mat_right.astype(jnp.float16)
            singvals_tot = singvals_tot.astype(jnp.float16)

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
                # Expanding bond dimension to comply with ideal hardware
                # settings
                dim = mat_left.shape[1]
                npad = ((0, 0), (0, cut - dim))
                mat_left = jnp.pad(
                    mat_left, npad, mode="constant", constant_values=(0, 0)
                )

                npad = ((0, cut - dim), (0, 0))
                mat_right = jnp.pad(
                    mat_right, npad, mode="constant", constant_values=(0, 0)
                )

                npad = (0, cut - dim)
                singvals = jnp.pad(
                    singvals, npad, mode="constant", constant_values=(0, 0)
                )

        else:
            singvals = singvals_tot
            singvals_cut = []  # xp.array([], dtype=self.dtype)
            cut = mat_left.shape[1]

        # Contract singular values if requested
        if svd_ctrl in ("D", "V", "R"):
            if contract_singvals.upper() == "L":
                mat_left = jnp.multiply(mat_left, singvals)
            elif contract_singvals.upper() == "R":
                key = "ij,i->ij"
                mat_right = jnp.einsum(key, mat_right, singvals)
            elif contract_singvals.upper() != "N":
                raise ValueError(
                    f"Contract_singvals option {contract_singvals} is not "
                    + "implemented. Choose between right (R), left (L) or None (N)."
                )

        # Reshape back to tensors
        tens_left = jnp.reshape(mat_left, list(shape_left) + [cut])
        if perm_left is not None:
            tens_left = jnp.transpose(tens_left, perm_left)

        tens_right = jnp.reshape(mat_right, [cut] + list(shape_right))
        if perm_right is not None:
            tens_right = jnp.transpose(tens_right, perm_right)

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

        other : instance of :class:`QteaJaxTensor`
            Links must match `self` up to the specified link.

        link : integer
            Stack along this link.

        **Returns**

        new_this : instance of :class:QteaJaxTensor`
        """
        newdim_self = list(self.shape)
        newdim_self[link] += other.shape[link]

        dim1, dim2, dim3 = self._shape_as_rank_3(link)
        dim4 = other.shape[link]

        new_dim = dim2 + dim4

        new_this = QteaJaxTensor(
            [dim1, new_dim, dim3], ctrl="N", dtype=self.dtype, device=self.device
        )
        # pylint: disable-next=protected-access
        new_this._elem = new_this.elem.at[:, :dim2, :].set(
            jnp.reshape(self.elem, [dim1, dim2, dim3])
        )
        # pylint: disable-next=protected-access
        new_this._elem = new_this.elem.at[:, dim2:, :].set(
            jnp.reshape(other.elem, [dim1, dim4, dim3])
        )
        new_this.reshape_update(newdim_self)

        return new_this

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

        new_this = QteaJaxTensor(
            new_dims, ctrl="N", dtype=self.dtype, device=self.device
        )
        # pylint: disable-next=protected-access
        new_this._elem = new_this._elem.at[:d1, :, :d3].set(
            self.elem.reshape([d1, d2, d3])
        )
        # pylint: disable-next=protected-access
        new_this._elem = new_this._elem.at[d1:, :, d3:].set(
            other.elem.reshape([i1, d2, i3])
        )
        new_this.reshape_update(newdim_self)

        return new_this

    # pylint: disable-next=unused-argument
    def tensordot(self, other, contr_idx, disable_streams=False):
        """Tensor contraction of two tensors along the given indices."""
        elem = jnp.tensordot(self._elem, other._elem, contr_idx)
        tens = QteaJaxTensor.from_elem_array(elem, dtype=self.dtype, device=self.device)
        return tens

    # pylint: disable-next=unused-argument
    def stream(self, disable_streams=False):
        """
        Get the instance of a context which can be used to parallelize.
        Disabled for jax so far and always returning the nullcontext.

        Parameters
        ----------

        disable_streams : bool, optional
            Allows to disable streams to avoid nested creation of
            streams. Globally, streams should be disabled via the
            `set_streams_*` function of the corresponding
            base tensor module (not available yet for jax).
            Default to False.

        Returns
        -------

        Context manager, i.e., always
        :class:`nullcontext(AbstractContextManager)`

        """

        return nullcontext()

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

    @staticmethod
    def get_default_datamover():
        """The default datamover compatible with this class."""
        return DataMoverJax()

    # --------------------------------------------------------------------------
    #                 Methods needed for _AbstractQteaBaseTensor
    # --------------------------------------------------------------------------

    def assert_diagonal(self, tol=1e-7):
        """Check that tensor is a diagonal matrix up to tolerance."""
        if self.ndim != 2:
            raise QRedTeaRankError("Not a matrix, hence not the identity.")

        tmp = jnp.diag(jnp.diag(self._elem))
        tmp -= self._elem

        if float(jnp.max(jnp.abs(tmp))) > tol:
            raise QRedTeaError("Matrix not diagonal.")

        return

    def assert_int_values(self, tol=1e-7):
        """Check that there are only integer values in the tensor."""
        tmp = jnp.round(self._elem)
        tmp -= self._elem

        if float(jnp.max(jnp.abs(tmp))) > tol:
            raise QRedTeaError("Matrix is not an integer matrix.")

        return

    def assert_real_valued(self, tol=1e-7):
        """Check that all tensor entries are real-valued."""
        tmp = jnp.imag(self._elem)

        if float(jnp.max(jnp.abs(tmp))) > tol:
            raise QRedTeaError("Tensor is not real-valued.")

    def concatenate_vectors(self, vectors, dtype, dim=None):
        """
        Concatenate vectors of the underlying numpy / cupy / torch / etc tensors.

        **Arguments***

        vectors : list
            List of one-dimensional arrays.

        dtype : data type
            Data type of concatenated vectors.

        dim : int | None
            Total dimension of concatenated vectors.
            If `None`, calculated on the fly.
            Default to `None`

        **Details**

        Used to concatenate singular values for symmetric tensors
        in SVD, which is needed as jax and tensorflow do not support
        `x[:]` assignments.
        """
        if dim is None:
            dim = 0
            for elem in vectors:
                dim += elem.shape[0]

        vec = self.vector_with_dim_like(dim, dtype=dtype)

        k2 = 0
        mapping = {}
        for ii, elem in enumerate(vectors):
            k1 = k2
            k2 += elem.shape[0]

            vec = vec.at[k1:k2].set(elem)
            mapping[ii] = (k1, k2)

        return vec, mapping

    def eig(self):
        """
        Compute eigenvalues and eigenvectors of a two-leg tensor

        Return
        ------
        eigvals, eigvecs : instances of :class:`QteaJaxTensor`
            Eigenvalues and corresponding eigenvectors of input tensor.
        """
        if self.ndim != 2:
            raise QRedTeaRankError("Works only with two-leg tensor")

        eigvals, eigvecs = jnp.linalg.eig(self.elem)
        eigvals = self.from_elem_array(eigvals, dtype=self.dtype, device=self.device)
        eigvecs = self.from_elem_array(eigvecs, dtype=self.dtype, device=self.device)
        return eigvals, eigvecs

    def expm(self, fuse_point=None, prefactor=1):
        """
        Take the matrix exponential with a scalar prefactor, i.e., Exp(prefactor * self).

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

        # Take the exponent and reshape back into the original shape.
        # pylint: disable-next=protected-access
        mat._elem = jax.scipy.linalg.expm(prefactor * mat.elem)
        mat.reshape_update(original_shape)
        return mat

    def elementwise_abs_smaller_than(self, value):
        """Return boolean if each tensor element is smaller than `value`"""
        return bool(jnp.all(jnp.abs(self._elem) < value))

    def _expand_tensor(self, link, new_dim, ctrl="R"):
        """Expand  tensor along given link and to new dimension."""
        newdim = list(self.shape)
        newdim[link] = new_dim - newdim[link]

        expansion = QteaJaxTensor(
            newdim, ctrl=ctrl, dtype=self.dtype, device=self.device
        )

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
        New QteaJaxTensor from array

        **Arguments**

        tensor : jaxlib.xla_extension.ArrayImpl
            Array for new tensor.

        dtype : data type, optional
            Can allow to specify data type.
            If not `None`, it will convert.
            Default to `None`
        """
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global xla_device

        if isinstance(tensor, np.ndarray):
            tensor = jnp.asarray(tensor)

        is_float = str(tensor.dtype) in [
            "complex64",
            "float64",
            "float16",
            "float32",
            "complex128",
        ]

        if dtype is None and (not is_float):
            warn(
                (
                    "Initializing a tensor with integer dtype can be dangerous "
                    "for the simulation. Please specify the dtype keyword in the "
                    "from_elem_array method if it was not intentional."
                )
            )

        if dtype is None:
            dtype = tensor.dtype
        if device is None:
            # We can actually check with JAX where we are running
            device = QteaJaxTensor.device_str(tensor)

        obj = cls(tensor.shape, ctrl=None, dtype=dtype, device=device)
        obj._elem = tensor

        obj.convert(dtype, device)

        return obj

    def get_attr(self, *args):
        """High-risk resolve attribute for an operation on an elementary array."""
        attributes = []

        for elem in args:
            if not hasattr(jnp, elem):
                raise QRedTeaError(
                    f"This tensor's elementary array does not support {elem}."
                )

            attributes.append(getattr(jnp, elem))

        if len(attributes) == 1:
            return attributes[0]

        return tuple(attributes)

    def get_argsort_func(self):
        """Return callable to argsort function."""
        return jnp.argsort

    def get_diag_entries_as_int(self):
        """Return diagonal entries of rank-2 tensor as integer on host."""
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global cpu_device

        if self.ndim != 2:
            raise QRedTeaRankError("Not a matrix, cannot get diagonal.")

        tmp = jnp.diag(self._elem)
        if self.device in ACCELERATOR_DEVICES:
            tmp = jax.device_put(tmp, device=cpu_device)

        tmp = jnp.real(tmp)

        return tmp.astype(jnp.int32)

    def get_sqrt_func(self):
        """Return callable to sqrt function."""
        return jnp.sqrt

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

        elem = jnp.einsum(subscipts, self._elem, other._elem).reshape(final_shape)
        tens = QteaJaxTensor.from_elem_array(elem, dtype=self.dtype, device=self.device)
        return tens

    def mask_to_device(self, mask):
        """
        Send a mask to the device where the tensor is.
        (right now only CPU --> GPU, CPU --> CPU).
        """
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global gpu_device, xla_device

        if self.is_cpu():
            return mask

        if self.is_gpu():
            mask_on_device = jax.device_put(mask, device=gpu_device)
            return mask_on_device

        if self.is_xla():
            mask_on_device = jax.device_put(mask, device=xla_device)
            return mask_on_device

        raise ValueError("Uknown device for converting mask.")

    def mask_to_host(self, mask):
        """
        Send a mask to the host where we need it for symmetric tensors, e.g.,
        degeneracies. Return as numpy.
        """
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global cpu_device
        if self.is_cpu():
            if isinstance(mask, jnp.ndarray):
                return np.asarray(mask)

            return mask

        if isinstance(mask, jnp.ndarray):
            mask_on_host = jax.device_put(mask, device=cpu_device)
        else:
            mask_on_host = mask

        return mask_on_host

    def permute_rows_cols_update(self, inds):
        """Permute rows and columns of rank-2 tensor with `inds`. Inplace update."""
        if self.ndim != 2:
            raise QRedTeaRankError(
                "Cannot only permute rows & cols for rank-2 tensors."
            )

        self._elem = self._elem[inds, :][:, inds]
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

        # Jax has no ARPACK
        kwargs["use_qtea_solver"] = True
        kwargs["injected_funcs"] = {"abs": jnp.abs}

        return kwargs, None, None

    def reshape(self, shape, **kwargs):
        """Reshape a tensor."""
        elem = jnp.reshape(self._elem, shape, **kwargs)
        tens = QteaJaxTensor.from_elem_array(elem, dtype=self.dtype, device=self.device)
        return tens

    def reshape_update(self, shape, **kwargs):
        """Reshape tensor dimensions inplace."""
        self._elem = jnp.reshape(self._elem, shape, **kwargs)

    def set_submatrix(self, row_range, col_range, tensor):
        """Set a submatrix of a rank-2 tensor for the given rows / cols."""

        if self.ndim != 2:
            raise QRedTeaRankError("Cannot only set submatrix for rank-2 tensors.")

        row1, row2 = row_range
        col1, col2 = col_range

        self._elem = self.elem.at[row1:row2, col1:col2].set(
            tensor.elem.reshape(row2 - row1, col2 - col1)
        )

    def subtensor_along_link(self, link, lower, upper):
        """
        Extract and return a subtensor select range (lower, upper) for one line.
        """
        dim1, dim2, dim3 = self._shape_as_rank_3(link)

        elem = jnp.reshape(self._elem, [dim1, dim2, dim3])
        elem = elem[:, lower:upper, :]

        new_shape = list(self.shape)
        new_shape[link] = upper - lower
        elem = jnp.reshape(elem, new_shape)

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

        subtensor : :class:`QteaJaxTensor`
            Subtensor with selected indices.

        Details
        -------

        The numpy equivalent is ``subtensor = tensor[:, :, inds, :]``
        for a rank-4 tensor and ``link=2``.
        """
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
            warn("Using default convergence parameters.")
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

        # Divide singvals in kept and cut
        singvals_kept = singvals[: min(cut, len(singvals))]
        singvals_cutted = singvals[min(cut, len(singvals)) :]
        # Renormalizing the singular values vector to its norm
        # before the truncation
        norm_kept = jnp.sum(singvals_kept**2)
        norm_trunc = jnp.sum(singvals_cutted**2)
        normalization_factor = jnp.sqrt(norm_kept) / jnp.sqrt(norm_kept + norm_trunc)
        singvals_kept /= normalization_factor

        # Renormalize cut singular values to track the norm loss
        singvals_cutted /= jnp.sqrt(norm_trunc + norm_kept)

        return cut, singvals_kept, singvals_cutted

    def _truncate_sv_ratio(self, singvals, conv_params):
        """
        Truncate the singular values based on the ratio
        with the biggest one.

        Parameters
        ----------
        singvals : jaxlib.xla_extension.ArrayImpl
            Array of singular values
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use in the procedure.

        Returns
        -------
        cut : int
            Number of singular values kept
        """
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global cpu_device

        lambda1 = singvals[0]
        cut = jnp.nonzero(singvals / lambda1 < conv_params.cut_ratio)[0]
        if self.device in ACCELERATOR_DEVICES:
            cut = jax.device_put(cut, device=cpu_device)

        chi_now = len(singvals)
        chi_by_conv = conv_params.max_bond_dimension
        chi_by_ratio = int(cut[0]) if len(cut) > 0 else chi_now
        chi_min = conv_params.min_bond_dimension

        return self._truncate_decide_chi(chi_now, chi_by_conv, chi_by_ratio, chi_min)

    def _truncate_sv_norm(self, singvals, conv_params):
        """
        Truncate the singular values based on the
        total norm cut.
        """
        raise NotImplementedError("Not yet for QteaJaxTensor.")

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
            Minimal chi to be conserved if possible.
        """
        return self._truncate_decide_chi_static(
            chi_now,
            chi_by_conv,
            chi_by_trunc,
            chi_min,
            _BLOCK_SIZE_BOND_DIMENSION,
            _BLOCK_SIZE_BYTE,
            self.elem.itemsize,
        )

    def vector_with_dim_like(self, dim, dtype=None):
        """Generate a vector in the native array of the base tensor."""
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global gpu_device, xla_device

        if dtype is None:
            dtype = self.dtype

        vec = jnp.zeros(dim, dtype=self.dtype)

        target_device = self.device
        if self.is_gpu(query=target_device):
            vec = jax.device_put(vec, device=gpu_device)
        elif self.is_xla(query=target_device):
            vec = jax.device_put(vec, device=xla_device)

        return vec

    # --------------------------------------------------------------------------
    #             Internal methods (not required by abstract class)
    # --------------------------------------------------------------------------

    @staticmethod
    def device_str(obj):
        """Resolve once the device for qteatftensor purposes as str."""
        device = str(obj.devices()).lower()
        if "cpu" in device:
            return _CPU_DEVICE

        if ("gpu" in device) or ("cuda" in device):
            return _GPU_DEVICE

        if "tpu" in device:
            return _XLA_DEVICE

        raise QRedTeaDeviceError(f"Device `{device}` not recognized.")

    @staticmethod
    def dtype_to_numpy(dtype):
        """Convert JAX dtype to numpy dtype."""

        if str(dtype) in ["float64", "<class 'jax.numpy.float64'>"]:
            return np.float64

        if str(dtype) in ["float32", "<class 'jax.numpy.float32'>"]:
            return np.float32

        if str(dtype) in ["float16", "<class 'jax.numpy.float16'>"]:
            return np.float16

        if str(dtype) in ["complex64", "<class 'jax.numpy.complex64'>"]:
            return np.complex64

        if str(dtype) in ["complex128", "<class 'jax.numpy.complex128'>"]:
            return np.complex128

        raise QRedTeaDataTypeError(
            f"JAX datatype `{dtype}` not available for numpy mapping."
        )

    def _split_qr_dim(self, rows, cols):
        """Split via QR knowing dimension of rows and columns."""
        if self.dtype == jnp.float16:
            matrix = self._elem.astype(jnp.float32).reshape(rows, cols)
        else:
            matrix = self._elem.reshape(rows, cols)

        qmat, rmat = jnp.linalg.qr(matrix)

        # from_elem_array will convert back to float16 if we converted before
        qtens = self.from_elem_array(qmat, dtype=self.dtype, device=self.device)
        rtens = self.from_elem_array(rmat, dtype=self.dtype, device=self.device)

        return qtens, rtens

    # pylint: disable-next=unused-argument
    def _split_svd_eigvl(self, matrix, svd_ctrl, max_bond_dimension, contract_singvals):
        """
        SVD of the matrix through an eigvenvalue decomposition.

        Parameters
        ----------
        matrix: jaxlib.xla_extension.ArrayImpl
            Matrix to decompose
        svd_crtl : str
            If "E" normal eigenvalue decomposition. If "X" use the sparse.
        max_bond_dimension : int
            Maximum bond dimension
        contract_singvals: str
            Whhere to contract the singular values

        Returns
        -------
        jaxlib.xla_extension.ArrayImpl
            Matrix U
        jaxlib.xla_extension.ArrayImpl
            Singular values
        jaxlib.xla_extension.ArrayImpl
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
            herm_mat = jnp.tensordot(matrix, jnp.conj(matrix), ([1], [1]))
        else:
            # contract_singvals == "L", the right tensor is unitary
            herm_mat = jnp.tensordot(jnp.conj(matrix), matrix, ([0], [0]))

        if svd_ctrl == "E":
            eigenvalues, eigenvectors = jnp.linalg.eigh(herm_mat)
        elif svd_ctrl == "X":
            warn("Falling back from X to E: jax has no eigsh.")
            eigenvalues, eigenvectors = jnp.linalg.eigh(herm_mat)
            # num_eigvl = min(herm_mat.shape[0] - 1, max_bond_dimension - 1)
            # eigenvalues, eigenvectors = jax.scipy.linalg.eigsh(herm_mat, k=num_eigvl)
        else:
            raise ValueError(
                f"svd_ctrl = {svd_ctrl} not valid with eigenvalue decomposition"
            )

        # Eigenvalues are sorted ascendingly, singular values descendengly
        # Only positive eigenvalues makes sense. Due to numerical precision,
        # there will be very small negative eigvl. We put them to 0.
        eigenvalues = eigenvalues.at[eigenvalues < 0].set(0)
        singvals = jnp.sqrt(eigenvalues[::-1][: min(matrix.shape)])
        eigenvectors = eigenvectors[:, ::-1]

        # Taking only the meaningful part of the eigenvectors
        if contract_singvals == "R":
            left = eigenvectors[:, : min(matrix.shape)]
            right = jnp.tensordot(jnp.conj(left), matrix, ([0], [0]))
        else:
            right = eigenvectors[:, : min(matrix.shape)]
            left = jnp.tensordot(matrix, right, ([1], [0]))
            right = jnp.conj(jnp.transpose(right, [1, 0]))

        return left, singvals, right

    def _split_svd_normal(self, matrix):
        """
        Normal SVD of the matrix. First try the faster gesdd iterative method.
        If it fails, resort to gesvd.

        Parameters
        ----------
        matrix: jaxlib.xla_extension.ArrayImpl
            Matrix to decompose

        Returns
        -------
        jaxlib.xla_extension.ArrayImpl
            Matrix U
        jaxlib.xla_extension.ArrayImpl
            Singular values
        jaxlib.xla_extension.ArrayImpl
            Matrix V^dagger
        """
        # Some differences to numpy calls
        mat_left, singvals_tot, mat_right = jnp.linalg.svd(matrix, full_matrices=False)

        return mat_left, singvals_tot, mat_right

    def _split_svd_random(self, matrix, max_bond_dimension):
        """
        SVD of the matrix through a random SVD decomposition
        as prescribed in page 227 of Halko, Martinsson, Tropp's 2011 SIAM paper:
        "Finding structure with randomness: Probabilistic algorithms for constructing
        approximate matrix decompositions"

        Parameters
        ----------
        matrix: jaxlib.xla_extension.ArrayImpl
            Matrix to decompose
        max_bond_dimension : int
            Maximum bond dimension

        Returns
        -------
        jaxlib.xla_extension.ArrayImpl
            Matrix U
        jaxlib.xla_extension.ArrayImpl
            Singular values
        jaxlib.xla_extension.ArrayImpl
            Matrix V^dagger
        """
        # pylint: disable-next=invalid-name,global-variable-not-assigned
        global gpu_device, xla_device, key_rng

        # pylint: disable-next=nested-min-max
        rank = min(max_bond_dimension, min(matrix.shape))
        # This could be parameterized but in the paper they use this
        # value
        n_samples = 2 * rank

        if self.is_dtype_complex():
            key_rng, subkey_r = jax.random.split(key_rng)
            rand_r = jax.random.normal(
                subkey_r, [matrix.shape[1], n_samples], dtype=jnp.float32
            )
            # rand_c = jax.random.normal(subkey_c, [matrix.shape[1], n_samples], dtype=jnp.float32)
            random = rand_r.astype(self.dtype)  # + 1j * rand_c.adtype(self.dtype)
        else:
            key_rng, subkey_r = jax.random.split(key_rng)
            random = jax.random.normal(
                subkey_r, [matrix.shape[1], n_samples], dtype=self.dtype
            )

        if self.is_gpu():
            random = jax.device_put(random, device=gpu_device)
        elif self.is_xla():
            random = jax.device_put(random, device=xla_device)

        reduced_matrix = jnp.dot(matrix, random)

        # Find orthonormal basis
        ortho, _ = jnp.linalg.qr(reduced_matrix)

        # Second part
        to_svd = jnp.dot(jnp.transpose(ortho, [1, 0]), matrix)
        left_tilde, singvals, right = jnp.linalg.svd(to_svd, full_matrices=False)

        left = jnp.dot(ortho, left_tilde)

        return left, singvals, right


def _scale_link_inverse_vector(link_weights):
    """Construct the inverse of singular values setting zeros to one."""
    # Have to handle zeros here ... as we allow padding singular
    # values with zeros, we must also automatically avoid division
    # by zero due to exact zeros. But we can assume it must be at
    # the end of the array
    if link_weights[-1] == 0.0:
        inds = jnp.where(link_weights == 0.0)
        vec = link_weights.at[inds].set(1.0)
        vec = 1 / vec
    else:
        vec = 1 / link_weights

    return vec


class DataMoverJax(_AbstractDataMover):
    """
    Data mover to move QteaJaxTensor between CPU and GPU.
    """

    tensor_cls = (QteaJaxTensor,)

    def __init__(self):
        pass

    @property
    def device_memory(self):
        """Current memory occupied in the device"""
        # return self.mempool.used_bytes()
        raise NotImplementedError("Jax data mover")

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
        warn("Moving still sync for Jax.")
        self.sync_move(tensor, device)

    def wait(self):
        """
        Put a barrier for the streams and wait them
        """
        # pylint: disable-next=unnecessary-pass
        pass


def default_jax_backend(device="cpu", dtype=jnp.complex64):
    """
    Generate a default tensor backend for symmetric tensors, i.e., with
    a :class:`QteaJaxTensor`.

    **Arguments**

    dtype : data type, optional
        Data type for JAX.
        Default to jax.complex64

    device : device specification, optional
        Default to `"cpu"`.
        Available: `"cpu", "gpu", "xla"`

    **Returns**

    tensor_backend : :class:`TensorBackend`
    """
    tensor_backend = TensorBackend(
        tensor_cls=QteaJaxTensor,
        base_tensor_cls=QteaJaxTensor,
        device=device,
        dtype=dtype,
        symmetry_injector=None,
        datamover=DataMoverJax(),
    )

    return tensor_backend


def default_abelian_jax_backend(device="cpu", dtype=jnp.complex128):
    """
    Provide a backend using jax and Abelian tensors.

    **Arguments**

    dtype : data type, optional
        Data type for JAX.
        Default to jax.complex64

    device : device specification, optional
        Default to `"cpu"`.
        Available: `"cpu", "gpu", "xla"`

    **Returns**

    tensor_backend : :class:`TensorBackend`
    """
    tensor_backend = TensorBackend(
        tensor_cls=QteaAbelianTensor,
        base_tensor_cls=QteaJaxTensor,
        device=device,
        dtype=dtype,
        symmetry_injector=AbelianSymmetryInjector(),
        datamover=DataMoverJax(),
    )

    return tensor_backend


# ------------------------------------------------------------------------------
#                                JIT compiled
# ------------------------------------------------------------------------------

# def _jit_add_inplace(this, other):
