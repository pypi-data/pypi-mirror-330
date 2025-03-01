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
Organize testing of formatting via black.
"""

import pathlib
import shlex
import subprocess
import unittest
from subprocess import PIPE, run


class TestFormatting(unittest.TestCase):
    """Test that black and isort formatting is implemented."""

    folders = "qredtea", "tests"

    def check_ext_util(self, cmd_call):
        """Run any external command via subprocess."""
        result = run(
            shlex.join(cmd_call), stderr=PIPE, shell=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_black_formatting(self):
        """Unit test to check if formatted according to black."""
        # Enter the following folders up to a defined depth
        depth = 1

        # Get the root path of the repository based on the current file
        root = str(pathlib.Path(__file__).parent.parent.resolve())

        paths = [root + "/*.py"]
        fill_path = "/"
        for _ in range(depth):
            for elem in self.folders:
                paths.append(root + "/" + elem + fill_path + "*.py")

            fill_path += "*/"

        cmd_call = ["black", "--check", "--exclude=Examples"] + paths
        result = subprocess.call(" ".join(cmd_call), shell=True)
        success = int(result) == 0

        self.assertTrue(success, "Repository did not pass Black formatting.")

    def test_isort(self):
        """Run the isort tool in the check mode."""
        self.check_ext_util(["isort", *self.folders, "--check"])
