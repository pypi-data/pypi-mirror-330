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
Integer and boolean arrays for symmetries wrap code to ensure integer only
arrays for symmetries in the qtealeaves module.
"""
import numpy as np

__all__ = [
    "iarray",
    "izeros",
    "imod",
    "indarray",
    "bmaskf",
    "bmaskt",
    "iany",
    "imaximum",
    "iminimum",
    "imin",
    "iargsort",
    "isum",
    "imax",
    "icumprod",
    "iall",
    "ikron",
    "i_int_type_list",
    "ichoice",
    "iabs",
    "iproduct",
    "ilogical_not",
    "iones",
]


def izeros(shape):
    """
    Create integer array of zeros.

    **Arguments**

    shape : ints
        Dimensions of the array.
    """
    return np.zeros(shape, dtype=int)


def iones(shape):
    """
    Create integer array of ones.

    **Arguments**

    shape : ints
        Dimensions of the array.
    """
    return np.ones(shape, dtype=int)


def iarray(array):
    """
    Convert the given list or array into an integer array.

    **Arguments**

    array : list, tuple, ndarray, etc
        Content of the integer array to be created.
    """
    return np.array(array, dtype=int)


def indarray(shape):
    """
    Create integer array without initialization.

    **Arguments**

    shape : ints
        Dimensions of the array.
    """
    return np.ndarray(shape, dtype=int)


def bmaskf(shape):
    """
    Create boolean array of zeros / false.

    **Arguments**

    shape : ints
        Dimensions of the array.
    """
    return np.zeros(shape, dtype=bool)


def bmaskt(shape):
    """
    Create boolean array of ones / true.

    **Arguments**

    shape : ints
        Dimensions of the array.
    """
    return np.ones(shape, dtype=bool)


def i_is_float(array):
    """
    Check if array is of floating data type.

    **Arguments**

    array : ndarray
    """
    return np.issubdtype(array.dtype, np.floating)


imod = np.mod
iany = np.any
iminimum = np.minimum
imin = np.min
imaximum = np.maximum
imax = np.max
iargsort = np.argsort
ikron = np.kron
isum = np.sum
iall = np.all
iproduct = np.prod
icumprod = np.cumprod
ichoice = np.random.choice
iabs = np.abs
ilogical_not = np.logical_not
ilogical_or = np.logical_or
i_isnan = np.isnan

i_int_type_list = [int, np.int32, np.int64]
