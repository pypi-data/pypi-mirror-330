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
Irrep listing module.
"""

# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches

from copy import deepcopy

import numpy as np

from qredtea.tooling import QRedTeaAbelianSymError, QRedTeaError

from .ibarrays import (
    bmaskf,
    bmaskt,
    i_is_float,
    i_isnan,
    iall,
    iany,
    iargsort,
    icumprod,
    ikron,
    ilogical_or,
    imax,
    imin,
    iminimum,
    indarray,
    isum,
)

__all__ = ["IrrepListing"]

RUN_SANITY_CHECKS = True


class IrrepListing:
    """
    IrrepListing contains a list of irreps.

    **Arguments**

    sym : instance of :class:`AbelianSymCombinedGroup`
        Combined symmetry group of the irreps.

    irreps : integer array, rank-2
        Irreps as integer labels. Each row contains one irrep.
        (For projectors, we allow floats. It has to be explicitly
        allowed in ``from_irreps`` via ``allow_dtype_float=True``.
        The equal sign accepts these including a wildcard `NaN`
        matching any irreps.)

    degeneracies : integer array, rank-1
        Degenercy of each irrep label.

    are_sorted : boolean, optional
        Flag if irreps are already sorted.
        Default to `False`

    remove_trivial : boolean, optional
        Flag if trivial irreps with degeneracy equal to
        zero should be removed.
        Default to `False`

    are_unique : boolean, optional
        Flag if irreps are already unique, if not duplicates
        will be removed and the degeneracy dimension summed up.
        Default to `False`.
    """

    def __init__(
        self,
        sym,
        irreps,
        degeneracies,
        are_sorted=False,
        remove_trivial=False,
        are_unique=False,
    ):
        if len(sym) != irreps.shape[1]:
            raise QRedTeaAbelianSymError(
                "Number of symmetries does not match individual irreps"
            )

        if degeneracies.ndim != 1:
            raise QRedTeaAbelianSymError(
                "Degeneracies are a vector for an irrep listing."
            )

        if len(degeneracies) != irreps.shape[0]:
            raise QRedTeaAbelianSymError(
                "Size degeneracies does not match size irreps."
            )

        self.sym = sym
        self.irreps = irreps
        self.degeneracies = degeneracies

        if not are_sorted:
            raise QRedTeaError("Use `from_irreps` ...")

        if remove_trivial:
            raise QRedTeaError("Use `from_irreps` ...")

        if not are_unique:
            raise QRedTeaError("Use `from_irreps` ...")
        if RUN_SANITY_CHECKS:
            tmp = []
            for elem in irreps:
                tmp += [tuple(elem)]

            if len(tmp) != len(set(tmp)):
                raise QRedTeaAbelianSymError("Claim of irreps being unique is wrong.")

        if self.irreps.flags.writeable:
            raise QRedTeaAbelianSymError("irreps cannot be writable.")

        if self.degeneracies.flags.writeable:
            raise QRedTeaAbelianSymError("degeneracies cannot be writable.")

        if len(self) > 1:
            inds = IrrepListing.argsort_irreps(irreps)
            if np.any(inds[1:] - inds[:-1] != 1):
                raise QRedTeaAbelianSymError("Not sorted.")

        self._hash = hash(self.sym)
        self._hash += hash(self.irreps.shape)
        self._hash += hash(tuple(self.irreps.flatten()))
        self._hash += hash(tuple(self.degeneracies.flatten()))

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    def has_degeneracies(self):
        """Flag if degeneracies exist in the irrep listing."""
        return iany(self.degeneracies > 1)

    # --------------------------------------------------------------------------
    #                          Overwritten operators
    # --------------------------------------------------------------------------

    # pylint: disable=invalid-name
    def phash(self, other, verbose=True):
        """Re-calculate the hash and compare. Returns `True` if equal."""
        h1 = hash(self.sym)
        h2 = hash(self.irreps.shape)
        h3 = hash(tuple(self.irreps.flatten()))
        h4 = hash(tuple(self.degeneracies.flatten()))

        o1 = hash(other.sym)
        o2 = hash(other.irreps.shape)
        o3 = hash(tuple(other.irreps.flatten()))
        o4 = hash(tuple(other.degeneracies.flatten()))

        if verbose:
            print("Checking hash self", self._hash, h1, h2, h3, h4)
            # pylint: disable-next=protected-access
            print("Checking hash other", other._hash, o1, o2, o3, o4)

        return (h1 + h2 + h3 + h4) == (o1 + o2 + o3 + o4)

    # pylint: enable=invalid-name

    def __eq__(self, other):
        """Comparing if instance of class is equal to another irrep listing."""
        # Problem beyond numpy tensors, hash comparison is not failing
        # return self._hash == other._hash

        val = self.phash(other, verbose=False)
        return val

    def __ne__(self, other):
        """Comparing if instance of class is different from another irrep listing."""
        return not (self == other)

    def __len__(self):
        """Length of irrep listing is represented by the number of irreps."""
        return self.irreps.shape[0]

    # --------------------------------------------------------------------------
    #                       classmethod, classmethod like
    # --------------------------------------------------------------------------

    @classmethod
    def from_irreps(
        cls,
        sym,
        irreps,
        degeneracies,
        are_sorted=False,
        remove_trivial=False,
        are_unique=False,
        allow_dtype_float=False,
    ):
        """Generate instance of IrrepListing through irreps and degeneracies."""
        if len(sym) != irreps.shape[1]:
            raise QRedTeaAbelianSymError(
                f"Number of symmetries ({len(sym)}) does not match "
                f"individual irreps ({irreps.shape[1]})."
            )

        if len(degeneracies) != irreps.shape[0]:
            raise QRedTeaAbelianSymError(
                "Size degeneracies does not match size irreps."
            )

        if (not allow_dtype_float) and i_is_float(irreps):
            raise QRedTeaAbelianSymError("Using floating point for irreps.")

        if not are_sorted:
            inds = cls.argsort_irreps(irreps)
            irreps = irreps[inds, :]
            degeneracies = degeneracies[inds]

        if remove_trivial:
            irreps, degeneracies = cls.mask_trivial(irreps, degeneracies)

        if not are_unique:
            irreps, degeneracies = cls.mask_non_unique(irreps, degeneracies)

        irreps.setflags(write=False)
        degeneracies.setflags(write=False)

        return cls(sym, irreps, degeneracies, are_sorted=True, are_unique=True)

    def intersection(self, other, deg_func=iminimum):
        """
        Intersection of an irrep listing with another irrep listing.

        **Arguments**

        other : instance of :class:`IrrepListing`
            Second irrep listing to build intersection.

        **Returns**

        irrep_listing : instance of :class:`IrrepListing`
            Contains the common irreps in `self` and `other`.
            Degneracy is build by taking the minimum.
        """
        if self.sym != other.sym:
            raise QRedTeaAbelianSymError("Mismatch in symmetries.")

        # index for irreps self
        mask_i = bmaskf(len(self))

        # index for irreps other
        mask_j = bmaskf(len(other))

        for ii, jj in self.iter_matches(other):
            mask_i[ii] = True
            mask_j[jj] = True

        irreps = self.irreps[mask_i, :]
        deg_i = self.degeneracies[mask_i]
        deg_j = other.degeneracies[mask_j]
        deg = deg_func(deg_i, deg_j)

        return IrrepListing.from_irreps(
            self.sym, irreps, deg, are_sorted=True, are_unique=True
        )

    def product_couple(self, other, invert_self=False, invert_other=False):
        """
        Build all combinations of irreps and couple them.

        **Arguments**

        other : instance of :class:`IrrepListing`
            Second set of irreps and degeneracies. Fast-moving index.

        invert_1 : boolean, optional
            Flag if irreps in `self` should be inverted.
            Default to `False`

        invert_2 : boolean, optional
            Flag if irreps in `other` should be inverted.
            Default to `False`

        **Returns**

        irrep_listing : instance of :class:`IrrepListing`

        **Details**

        Method is the equivalent of itertools.product for two irreps.
        Degeneracies are the product between degeneracy of irrep
        in `self` and `other`.
        """
        irreps = self.sym.product_couple_irreps(
            self.irreps,
            other.irreps,
            invert_1=invert_self,
            invert_2=invert_other,
        )

        deg_new = ikron(self.degeneracies, other.degeneracies).flatten()

        return IrrepListing.from_irreps(self.sym, irreps, deg_new)

    def union(self, other):
        """
        Union of an irrep listing with another irrep listing.

        **Arguments**

        other : instance of :class:`IrrepListing`
            Second irrep listing to build union.

        **Returns**

        irrep_listing : instance of :class:`IrrepListing`
            Contains the irreps of `self` and `other`
            Degeneracy is sum of degeneracy in `self` and
            in `other` if irreps appears in both.
        """
        if self.sym != other.sym:
            raise QRedTeaAbelianSymError("Mismatch in symmetries.")

        # index for irreps self
        deg_i = deepcopy(self.degeneracies)

        # index for irreps other
        mask_j = bmaskt(len(other))

        for ii, jj in self.iter_matches(other):
            deg_i[ii] += other.degeneracies[jj]
            mask_j[jj] = False

        shape = (len(self) + isum(mask_j), len(self.sym))
        irreps = indarray(shape)
        irreps[: len(self), :] = self.irreps
        irreps[len(self) :, :] = other.irreps[mask_j, :]

        deg = indarray(shape[0])
        deg[: len(self)] = deg_i
        deg[len(self) :] = other.degeneracies[mask_j]

        return IrrepListing.from_irreps(self.sym, irreps, deg, are_unique=True)

    # --------------------------------------------------------------------------
    #                            Checks and asserts
    # --------------------------------------------------------------------------

    def sanity_check(self):
        """Sanity check to verify properties of irrep listing."""
        if len(self.sym) != self.irreps.shape[1]:
            raise QRedTeaAbelianSymError(
                "Number of symmetries does not match individual irreps"
            )

        if len(self.degeneracies) != self.irreps.shape[0]:
            raise QRedTeaAbelianSymError(
                "Size degeneracies does not match size irreps."
            )

    def is_dtype_float(self):
        """Return if irreps is of data type float (only allowed for projectors)."""
        return i_is_float(self.irreps)

    # --------------------------------------------------------------------------
    #                            Remaining methods
    # --------------------------------------------------------------------------

    def index(self, irrep, start_idx=0, require_match=False):
        """
        Search of irrep similar to `index` method of a python list.

        **Arguments**

        irrep : integer array, rank-1
            Search this irrep and return its index in irrep listing.

        start_idx : int, optional
            Speed-up search by specifying start index if it
            is known that irrep is not contained in indices
            (0 ... start_idx - 1).
            Default to 0 (searching complete irrep listing until match)

        **Returns**

        idx : int or None
            Returns row of match or `None` if no match given.
        """
        # Can be improved by better search.
        for ii in range(start_idx, len(self)):
            if self.is_equal_irrep(self.irreps[ii, :], irrep):
                return ii

        if require_match:
            print("Error information", irrep, self.irreps)
            raise QRedTeaAbelianSymError("Irrep not found.")

        return None

    @staticmethod
    def argsort_irreps(irreps):
        """
        Argsort similar to numpy's argsort for and irreps array.

        **Arguments**

        irreps : integer array, rank-2
            Irreps to be sorted row-by-row.

        **Returns**

        inds : integer array, rank-1
            Such that irreps[inds, :] sorts the irreps
            ascendingly.
        """
        # Offset with minima along each symmetry, calculate dimension
        # and combine into one index.
        dmin = imin(irreps, axis=0)
        tmp = irreps - dmin
        dmax = imax(tmp, axis=0) + 1
        dcum = icumprod(dmax[::-1])[::-1]
        dcum[:-1] = dcum[1:]
        dcum[-1] = 1

        tmp1 = tmp.dot(dcum)
        inds = iargsort(tmp1)

        return inds

        # Avoids some math, but has bug inside
        # n2 = irreps.shape[1]
        # if n2 > 1:
        #    set_ind = set(list(irreps[:, 0]))
        #    for elem in set_ind:
        #        mask = irreps[:, 0] == elem
        #        sub_irreps = irreps[mask, 1:]
        #        inds_sub = IrrepListing.argsort_irreps(sub_irreps)
        #        inds[mask] = inds[mask][inds_sub]
        # return inds

    @staticmethod
    def get_mask_non_unique(irreps):
        """True for first appearance of each irrep."""
        mask = bmaskt(irreps.shape[0])
        mask[1:] = isum(irreps[1:, :] != irreps[:-1, :], axis=1) > 0

        return mask

    @staticmethod
    def is_equal_irrep(irrep_a, irrep_b):
        """Check if two irreps (integer array, rank-1) are equal."""
        if (not i_is_float(irrep_b)) and (not i_is_float(irrep_a)):
            return iall(irrep_a == irrep_b)

        arr_eq = irrep_a == irrep_b

        if i_is_float(irrep_b):
            arr_na = i_isnan(irrep_b)
            arr_eq = ilogical_or(arr_eq, arr_na)

        if i_is_float(irrep_a):
            arr_na = i_isnan(irrep_a)
            arr_eq = ilogical_or(arr_eq, arr_na)

        return iall(arr_eq)

    @staticmethod
    def is_smaller_irrep(irrep_a, irrep_b):
        """Check if irrep_a is smaller than irrep_b (integer array, rank-1)."""
        is_smaller = irrep_a < irrep_b
        is_greater = irrep_a > irrep_b

        for ii, elem in enumerate(is_greater):
            if elem:
                return False

            if is_smaller[ii]:
                return True

        # all elements are equal
        return False

    @staticmethod
    def is_greater_irrep(irrep_a, irrep_b):
        """Check if irrep_a is greater than irrep_b (integer array, rank-1)."""
        is_smaller = irrep_a < irrep_b
        is_greater = irrep_a > irrep_b

        for ii, elem in enumerate(is_greater):
            if elem:
                return True

            if is_smaller[ii]:
                return False

        # all elements are equal
        return False

    @staticmethod
    def mask_non_unique(irreps, degeneracies):
        """
        Modify irrep listing such that only unique irreps are present.

        **Details**

        Degeneracy dimension is additive. Update is inplace.
        """
        mask = IrrepListing.get_mask_non_unique(irreps)

        idx = None
        for ii, mask_ii in enumerate(mask):
            if mask_ii:
                idx = ii
            else:
                degeneracies[idx] += degeneracies[ii]

        irreps = irreps[mask, :]
        degeneracies = degeneracies[mask]

        return irreps, degeneracies

    @staticmethod
    def mask_trivial(irreps, degeneracies):
        """Inplace-update masking all trivial irreps with deneracy zero."""
        if len(degeneracies) != irreps.shape[0]:
            raise QRedTeaAbelianSymError("Dimension mismatch irreps and degeneracies.")

        mask = degeneracies != 0
        irreps = irreps[mask]
        degeneracies = degeneracies[mask]

        return irreps, degeneracies

    def iter_matches(self, other):
        """
        Iteration of the matche of an irrep listing with another
        irrep listing by their integer indices

        **Arguments**

        other : instance of :class:`IrrepListing`
            Search for matches between `self` and irrep listing `other`

        **Returns**

        (ii, jj)
            ii is index of matching irrep in `self`
            jj is index of matching irrep in `other`
            Iterator yields matches in pairs via loop.
        """
        nn = len(self) + len(other)

        if len(self) == 0 or len(other) == 0:
            return

        # index for irreps self
        ii = 0
        irrep_ii = self.irreps[0, :]

        # index for irreps other
        jj = 0
        irrep_jj = other.irreps[0, :]

        for _ in range(nn):
            if self.is_equal_irrep(irrep_ii, irrep_jj):
                # Match, increment both (should be unique here)
                yield ii, jj

                ii += 1
                jj += 1

                if (ii == len(self)) or (jj == len(other)):
                    break

                irrep_ii = self.irreps[ii, :]
                irrep_jj = other.irreps[jj, :]

            elif self.is_smaller_irrep(irrep_ii, irrep_jj):
                ii += 1

                if ii == len(self):
                    break

                irrep_ii = self.irreps[ii, :]
            elif self.is_greater_irrep(irrep_ii, irrep_jj):
                jj += 1

                if jj == len(other):
                    break

                irrep_jj = other.irreps[jj, :]
            else:
                raise QRedTeaError("What else can there be???")

    def print_full(self, indent=0):
        """Print all information on irrep listing."""
        prefix = " " * indent
        print(prefix + "-" * 10 + " IrrepListing " + "-" * 10)
        print(prefix + "Symmetry:", self.sym)
        for ii, irrep in enumerate(self.irreps):
            print(
                prefix + "    irrep", ii, "qnums", irrep, "deg", self.degeneracies[ii]
            )
        print(prefix + "^" * 34)
