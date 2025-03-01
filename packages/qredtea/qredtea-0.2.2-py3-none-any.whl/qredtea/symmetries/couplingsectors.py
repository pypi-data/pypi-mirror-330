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
Coupling sectors module.
"""

from qredtea.tooling import QRedTeaAbelianSymError, QRedTeaLinkError, QRedTeaRankError

from .ibarrays import bmaskf, i_int_type_list, iall, iany, izeros

__all__ = ["CouplingSectors"]

RUN_SANITY_CHECKS = True


class CouplingSectors:
    """
    Coupling sectors are defined over a given set of links and their irreps. A
    coupling sector for one link is the index of the corresponding irrep, i.e.,
    a matching coupling sector means matching irrep.

    **Arguments**

    sectors : np.ndarray of rank-2
        First index loops of coupling sectors.
        Second index loops over links.
        A rank-3 tensor with 10 subtensors should have dimensions 10 x 3.

    sorted_for : integer list or `None`, optional
        Indicate if coupling sectors are already sorted for a list of links.
        Default to `None` (not sorted for any links).
    """

    def __init__(self, sectors, sorted_for=None):
        self.denormalized_sectors = sectors

        if len(sectors.shape) != 2:
            raise QRedTeaRankError("sectors must be rank-2 over sectors and links.")

        self.sorted_for = sorted_for
        self.hashed_for = None
        self.hash_table = None
        self.tracker = bmaskf(self.num_coupling_sectors)

        # self.sanity_check()

    @property
    def num_coupling_sectors(self):
        """Number of coupling sectors."""
        return self.denormalized_sectors.shape[0]

    def reset_tracker(self):
        """Tracker will be reset to `False`."""
        self.tracker[:] = False

    def iter_tracker_accessed(self):
        """Iterate over all row-indices and coupling sectors where tracker is true."""
        for ii, value in self.tracker:
            if value:
                yield ii, self.denormalized_sectors[ii, :]

    def depreceated_iter_tracker_skipped(self):
        """Iterate over all row-indices and coupling sectors where tracker is false."""
        for ii, value in self.tracker:
            if not value:
                yield ii, self.denormalized_sectors[ii, :]

    def iter_tracker_false(self):
        """Iterate over all row-indices and coupling sectors where tracker is false."""
        for ii in range(self.num_coupling_sectors):
            if not self.tracker[ii]:
                yield ii, self.denormalized_sectors[ii, :]

    def iter_sectors(self):
        """Iterate over all row-indices and coupling sectors."""
        for ii in range(self.num_coupling_sectors):
            yield ii, self.denormalized_sectors[ii, :]

    def __getitem__(self, key, default=None):
        """Lookup of coupling sector after setting hashes. None if not present."""
        if default is None:
            default = [None]
        if self.hashed_for is None:
            raise QRedTeaAbelianSymError(
                "Trying to access hashed elements without ever generating them."
            )
        key_as_tuple = tuple(key)
        idx = self.hash_table.get(key_as_tuple, default)
        if idx[0] is not None:
            self.tracker[idx] = True
        return idx

    def sanity_check(self):
        """Checking validity of :class:`CouplingSectors`."""
        if not RUN_SANITY_CHECKS:
            return

        if self.denormalized_sectors.dtype not in i_int_type_list:
            raise QRedTeaAbelianSymError(
                "Sectors need to be of type int, but "
                + f"{self.denormalized_sectors.dtype}."
            )

        dim = self.denormalized_sectors.shape[1]
        for ii in range(dim):
            cs_group = self.denormalized_sectors.copy()
            cs_group[:, ii] = 0

            cs_one = self.denormalized_sectors[:, ii]

            check = {}
            for jj in range(self.num_coupling_sectors):
                key = tuple(cs_group[jj, :])

                ref = check.get(key, None)
                if ref is None:
                    check[key] = cs_one[jj]
                elif ref != cs_one[jj]:
                    raise QRedTeaAbelianSymError("Coupling sector invalid.")

    def transpose(self, permutation):
        """Permute the columns of a CS and return new :class:`CouplingSectors`."""
        sectors = self.denormalized_sectors[:, permutation]
        return CouplingSectors(sectors)

    def generate_hashes(self, hash_links):
        """Generate the hashed for `__getitem__` with the links passed."""
        self.tracker[:] = False
        if iall(self.hashed_for == hash_links):
            return

        self.hashed_for = hash_links
        self.hash_table = {}

        for ii in range(self.num_coupling_sectors):
            key = tuple(self.denormalized_sectors[ii, hash_links])

            if key in self.hash_table:
                self.hash_table[key].append(ii)
            else:
                self.hash_table[key] = [ii]

    def get_col(self, idx):
        """Extract one column of the coupling sectors, requested via `idx`."""
        return self.denormalized_sectors[:, idx]

    def attach_dummy_link(self, position):
        """Attach a dummy link, i.e., coupling sector zero. Inplace update."""
        d1, d2 = self.denormalized_sectors.shape
        sectors = izeros((d1, d2 + 1))

        sectors[:, :position] = self.denormalized_sectors[:, :position]
        sectors[:, position + 1 :] = self.denormalized_sectors[:, position:]

        self.denormalized_sectors = sectors

    def remove_dummy_link(self, position):
        """Remove dummy link at given position; required to be zero. Inplace update."""
        d1, d2 = self.denormalized_sectors.shape
        sectors = izeros((d1, d2 - 1))

        if iany(self.denormalized_sectors[:, position] != 0):
            raise QRedTeaLinkError("Probably not a dummy link.")

        sectors[:, :position] = self.denormalized_sectors[:, :position]
        sectors[:, position:] = self.denormalized_sectors[:, position + 1 :]

        self.denormalized_sectors = sectors
