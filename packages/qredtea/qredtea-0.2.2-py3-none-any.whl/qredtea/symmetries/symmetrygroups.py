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
Symmetry groups defined the Abelian symmetries and combined Abelian symmetry groups.
"""

import abc
from dataclasses import dataclass, field

from qredtea.tooling import QRedTeaAbelianSymError

from .ibarrays import iarray, imod, izeros

__all__ = [
    "_AbstractAbelianSymGroup",
    "AbelianSymZN",
    "AbelianSymU1",
    "AbelianSymCombinedGroup",
]


class _AbstractAbelianSymGroup(abc.ABC):
    """
    Abstract Abelian symmetry group from which actual Abelian symmetries
    can be derived.
    """

    # def __ne__(self, other):
    #    """Comparing if instance of class is different from another symmetry."""
    #    return not (self == other)

    @abc.abstractmethod
    def __str__(self):
        """String representation of symmetry."""

    @abc.abstractmethod
    def __repr__(self):
        """String representation of symmetry."""

    # @abc.abstractmethod
    # def __eq__(self, other):
    #    """Comparing if instance of class is equal to another symmetry."""

    @abc.abstractmethod
    def __contains__(self, irrep_label):
        """Check if an irrep is part of this symmetry."""

    @property
    @abc.abstractmethod
    def identical_irrep(self):
        """Identical irrep which does not change charge / sector."""

    @abc.abstractmethod
    def invert_irrep(self, irrep):
        """Invert the irrep passed as argument according to the symmetry's rule."""

    @abc.abstractmethod
    def couple_irrep(self, irrep1, irrep2):
        """Couple the two irreps passed as argument according to the symmetry's rule."""

    @abc.abstractmethod
    def decouple_irrep(self, irrep1, irrep2):
        """Decouple the two irreps passed as argument according to the symmetry's rule."""

    @abc.abstractmethod
    def couple_multiple(self, irrep_vec, invert_irreps=False):
        """Deprecated."""


@dataclass(frozen=True)
class AbelianSymZN(_AbstractAbelianSymGroup):
    """
    Abelian symmetry of Zn group.

    **Arguments**

    order : int
        Order of the Zn symmetry, i.e., possible irreps
        range from 0 to (order - 1).
    """

    order: int
    sym: str = field(default="Zn")

    # def __init__(self, order):
    #    self.order = order

    def __post_init__(self):
        if self.sym != "Zn":
            raise QRedTeaAbelianSymError("U1 symmetry needs symmetry string to be U1.")

    def __str__(self):
        """String representation of Zn symmetry."""
        return "Z%d" % (self.order)

    def __repr__(self):
        """String representation of Zn symmetry."""
        return "Z%d" % (self.order)

    # def __eq__(self, other):
    #    """Comparing if instance of class is equal to another symmetry."""
    #    if not isinstance(other, AbelianSymZN):
    #        return False

    #    return self.order == other.order

    def __contains__(self, irrep_label):
        """Check if an irrep is part of this symmetry."""
        return 0 <= irrep_label < self.order

    @property
    def identical_irrep(self):
        """Identical irrep which does not change charge / sector."""
        return 0

    def invert_irrep(self, irrep):
        """Invert the irrep passed as argument according to the symmetry's rule."""
        return imod(-irrep, self.order)

    def couple_irrep(self, irrep1, irrep2):
        """Couple the two irreps passed as argument according to the symmetry's rule."""
        return imod(irrep1 + irrep2, self.order)

    def decouple_irrep(self, irrep1, irrep2):
        """Decouple the two irreps passed as argument according to the symmetry's rule."""
        return imod(irrep1 - irrep2, self.order)

    def couple_multiple(self, irrep_vec, invert_irreps=False):
        """Deprecated."""
        if invert_irreps:
            irrep_vec *= -1

        irrep = irrep_vec[0]
        for elem in irrep_vec[1:]:
            irrep += elem

        if invert_irreps:
            irrep_vec *= -1

        # return imod(irrep, self.order)
        raise QRedTeaAbelianSymError("Untested and unused so far.")


@dataclass(frozen=True)
class AbelianSymU1(_AbstractAbelianSymGroup):
    """
    Abelian symmetry of U(1) group.

    **Arguments**

    No arguments.
    """

    sym: str = field(default="U1")

    def __post_init__(self):
        if self.sym != "U1":
            raise QRedTeaAbelianSymError("U1 symmetry needs symmetry string to be U1.")

    def __str__(self):
        """String representation of U(1) symmetry."""
        return "U1"

    def __repr__(self):
        """String representation of U(1) symmetry."""
        return "U1"

    # def __eq__(self, other):
    #    """Comparing if instance of class is equal to another symmetry."""
    #    return isinstance(other, AbelianSymU1)

    def __contains__(self, irrep):
        """Check if an irrep is part of this symmetry."""
        return True

    @property
    def identical_irrep(self):
        """Identical irrep which does not change charge / sector."""
        return 0

    def invert_irrep(self, irrep):
        """Invert the irrep passed as argument according to the symmetry's rule."""
        return -irrep

    def couple_irrep(self, irrep1, irrep2):
        """Couple the two irreps passed as argument according to the symmetry's rule."""
        return irrep1 + irrep2

    def decouple_irrep(self, irrep1, irrep2):
        """Decouple the two irreps passed as argument according to the symmetry's rule."""
        return irrep1 - irrep2

    def couple_multiple(self, irrep_vec, invert_irreps=False):
        """Deprecated."""
        if invert_irreps:
            irrep_vec *= -1

        irrep = irrep_vec[0]
        for elem in irrep_vec[1:]:
            irrep += elem

        if invert_irreps:
            irrep_vec *= -1

        # return irrep
        raise QRedTeaAbelianSymError("Untested and unused so far.")


class AbelianSymCombinedGroup(tuple):
    """
    List of one or multiple Abelian symmetries used within a simulation.
    """

    def __new__(cls, *args):
        if len(args) == 1 and hasattr(args[0], "__len__"):
            args = args[0]

        for elem in args:
            if not isinstance(elem, _AbstractAbelianSymGroup):
                raise TypeError(
                    f"Entries must be AbelianSymGroup., but got {type(elem)}."
                )

        return tuple.__new__(AbelianSymCombinedGroup, tuple(args))

    def __contains__(self, irrep):
        """Check if an irrep is part of this combined symmetry."""
        for ii, elem in enumerate(self):
            if irrep[ii] not in elem:
                return False

        return True

    @property
    def identical_irrep(self):
        """Identical irrep which does not change charge / sector."""
        return iarray([self[ii].identical_irrep for ii in range(len(self))])

    def invert_irrep(self, irrep):
        """
        Invert the irrep passed as argument according to the symmetry's rule.

        **Arguments**

        irrep : integer array
            either single irrep (rank-1) or multiple (rank-2)

        """
        if irrep.ndim == 1:
            return self._invert_single_irrep(irrep)

        return self._invert_multiple_irreps(irrep)

    def _invert_single_irrep(self, irrep):
        """Invert single irrep passed as argument according to the symmetry's rule."""
        nn = len(self)
        inv_irrep = izeros(nn)

        for ii, sym in enumerate(self):
            inv_irrep[ii] = sym.invert_irrep(irrep[ii])

        return inv_irrep

    def _invert_multiple_irreps(self, irreps):
        """Invert irreps passed as argument row-by-row according to the symmetry's rule."""
        inv_irrep = izeros(irreps.shape)

        for ii, sym in enumerate(self):
            inv_irrep[:, ii] = sym.invert_irrep(irreps[:, ii])

        return inv_irrep

    def couple_irreps(self, irrep1, irrep2):
        """
        Couple the irreps passed as argument according to the symmetry's rule.

        **Arguments**

        irrep1 : integer array
            either single irrep (rank-1) or multiple (rank-2)

        irrep2 : integer array
            either single irrep (rank-1) or multiple (rank-2)
        """
        if (irrep1.ndim == 1) and (irrep2.ndim == 1):
            return self._couple_irrep_irrep(irrep1, irrep2)

        if (irrep1.ndim == 2) and (irrep2.ndim == 1):
            return self._couple_irreps_irrep(irrep1, irrep2)

        if (irrep1.ndim == 1) and (irrep2.ndim == 2):
            return self._couple_irrep_irreps(irrep1, irrep2)

        if (irrep1.ndim == 2) and (irrep2.ndim == 2):
            if irrep1.shape[0] == 1:
                return self._couple_irrep_irreps(irrep1[0, :], irrep2)

            if irrep2.shape[0] == 1:
                return self._couple_irreps_irrep(irrep1, irrep2[0, :])

        raise ValueError(
            f"Dimension irreps not available: {irrep1.shape}, {irrep2.shape}"
        )

    def _couple_irrep_irrep(self, irrep1, irrep2):
        """Couple single irreps according to symmetry."""
        nn = len(self)
        irrep = izeros(nn)

        for ii in range(nn):
            irrep[ii] = self[ii].couple_irrep(irrep1[ii], irrep2[ii])

        return irrep

    def _couple_irreps_irrep(self, irreps1, irrep2):
        """Couple multiple irreps with single irreps according to symmetry."""
        irrep = izeros(irreps1.shape)

        for ii, sym in enumerate(self):
            irrep[:, ii] = sym.couple_irrep(irreps1[:, ii], irrep2[ii])

        return irrep

    def _couple_irrep_irreps(self, irrep1, irreps2):
        """Couple single irrep with multiple irreps according to symmetry."""
        irrep = izeros(irreps2.shape)

        for ii, sym in enumerate(self):
            irrep[:, ii] = sym.couple_irrep(irrep1[ii], irreps2[:, ii])

        return irrep

    def product_couple_irreps(self, irreps1, irreps2, invert_1=False, invert_2=False):
        """
        Build all combinations of irreps and couple them.

        **Arguments**

        irreps1 : integer array, rank-2
            First set of irreps.

        irreps2 : integer array, rank-2
            Second set of irreps. Fast-moving index.

        invert_1 : boolean, optional
            Flag if irreps1 should be inverted.
            Default to `False`

        invert_2 : boolean, optional
            Flag if irreps2 should be inverted.
            Default to `False`

        **Returns**

        irreps : integer arrray, rank-2

        **Details**

        Method is the equivalent of itertools.product for two irreps.
        """
        n1 = irreps1.shape[0]
        n2 = irreps2.shape[0]

        if invert_1:
            irreps_a = self.invert_irrep(irreps1)
        else:
            irreps_a = irreps1

        if invert_2:
            irreps_b = self.invert_irrep(irreps2)
        else:
            irreps_b = irreps2

        i1 = 0
        i2 = n1
        irreps = izeros((n1 * n2, irreps1.shape[1]))

        for ii in range(n2):
            irreps[i1:i2, :] = self.couple_irreps(irreps_a, irreps_b[ii, :])
            i1 += n1
            i2 += n1

        return irreps

    def decouple_irreps(self, irrep1, irrep2):
        """
        Decouple the irreps passed as argument according to the symmetry's rule.

        **Arguments**

        irrep1 : integer array
            either single irrep (rank-1) or multiple (rank-2)

        irrep2 : integer array
            either single irrep (rank-1) or multiple (rank-2)
        """
        if (irrep1.ndim == 1) and (irrep2.ndim == 1):
            return self._decouple_irrep(irrep1, irrep2)

        if (irrep1.ndim == 2) and (irrep2.ndim == 1):
            return self._decouple_irreps_irrep(irrep1, irrep2)

        if (irrep1.ndim == 1) and (irrep2.ndim == 2):
            return self._decouple_irrep_irreps(irrep1, irrep2)

        raise ValueError("Dimension irreps not available.")

    def _decouple_irrep(self, irrep1, irrep2):
        """Decouple single irreps according to symmetry."""
        irrep = izeros(len(self))

        for ii, sym in enumerate(self):
            irrep[ii] = sym.decouple_irrep(irrep1[ii], irrep2[ii])

        return irrep

    def _decouple_irreps_irrep(self, irreps1, irrep2):
        """Decouple multiple irreps with single irreps according to symmetry."""
        irrep = izeros(irreps1.shape)

        for ii, sym in enumerate(self):
            irrep[:, ii] = sym.decouple_irrep(irreps1[:, ii], irrep2[ii])

        return irrep

    def _decouple_irrep_irreps(self, irrep1, irreps2):
        """Decouple single irrep with multiple irreps according to symmetry."""
        irrep = izeros(irreps2.shape)

        for ii, sym in enumerate(self):
            irrep[:, ii] = sym.decouple_irrep(irrep1[ii], irreps2[:, ii])

        return irrep
