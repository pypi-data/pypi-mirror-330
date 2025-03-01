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
Tensors submodule init for tensorflow tensors.
"""

from functools import partial

from qredtea.tooling import (
    QRedTeaBackendLibraryImportError,
    assert_module_available,
    get_error_tensor_class,
)

# All modules have an __all__ defined
try:
    from .qteatftensor import *
except QRedTeaBackendLibraryImportError:
    # All the classes/functions are overwritten with a function that simply
    # raises an error when calleds
    assert_tf_available = partial(assert_module_available, module="tensorflow")
    QteaTFTensor = get_error_tensor_class(assert_tf_available)
    default_tensorflow_backend = assert_tf_available
    default_abelian_tensorflow_backend = assert_tf_available
    set_block_size_qteatftensors = assert_tf_available
    DataMoverTensorflow = assert_tf_available
