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
Exception classes for quantum red tea.
"""

import importlib

__all__ = [
    "QRedTeaError",
    "QRedTeaEmptyTensorError",
    "QRedTeaLinkError",
    "QRedTeaRankError",
    "QRedTeaAbelianSymError",
    "QRedTeaDeviceError",
    "QRedTeaDataTypeError",
    "QRedTeaBackendLibraryImportError",
    "QRedTeaLinAlgError",
    "assert_module_available",
    "get_error_tensor_class",
]


class QRedTeaError(Exception):
    """Generic error for the qredtea library."""


class QRedTeaEmptyTensorError(QRedTeaError):
    """Erros induced by empty tensors, parsed or generated."""


class QRedTeaLinkError(QRedTeaError):
    """Errors induced by problems with the link."""


class QRedTeaRankError(QRedTeaError):
    """Errors induced by passing the wrong rank of a tensor."""


class QRedTeaAbelianSymError(QRedTeaError):
    """Errors induced by symmetries."""


class QRedTeaDeviceError(QRedTeaError):
    """Errors induced by device selection, conversion."""


class QRedTeaDataTypeError(QRedTeaError):
    """Errors induced by device conversion of data types."""


class QRedTeaBackendLibraryImportError(QRedTeaError, ImportError):
    """Errors induced by not being able to import a library."""


class QRedTeaLinAlgError(QRedTeaError):
    """Errors introduced by linear algebra routines."""


def assert_module_available(*args, **kwargs):
    """Function to punish those that try to use JAX without installing it."""
    module = kwargs.get("module", "numpy")
    if importlib.util.find_spec(module) is None:
        raise QRedTeaBackendLibraryImportError(f"{module} could not be imported.")


def get_error_tensor_class(error_function):
    """Return a class that gives errors when any of the class/static methods are called"""

    class ErrorTensor:
        """
        Class to handle all the possible
        """

        func = error_function

        def __init__(self, *args, **kwargs):
            self.func()

        @staticmethod
        def convert_operator_dict(*args, **kwargs):
            """Raise the error"""
            error_function()

        @staticmethod
        def dummy_link(*args, **kwargs):
            """Raise the error"""
            error_function()

        @staticmethod
        def set_missing_link(*args, **kwargs):
            """Raise the error"""
            error_function()

        @staticmethod
        def device_str(*args, **kwargs):
            """Raise the error"""
            error_function()

        @staticmethod
        def dtype_to_numpy(*args, **kwargs):
            """Raise the error"""
            error_function()

        @classmethod
        def from_qteatensor(cls, *args, **kwargs):
            """Raise the error"""
            cls.func()

        @classmethod
        def read(cls, *args, **kwargs):
            """Raise the error"""
            cls.func()

        @classmethod
        def mpi_recv(cls, *args, **kwargs):
            """Raise the error"""
            cls.func()

        @classmethod
        def from_elem_array(cls, *args, **kwargs):
            """Raise the error"""
            cls.func()

    return ErrorTensor
