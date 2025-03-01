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
Tensors submodule init for tensors via torch.
"""

from functools import partial

from qredtea.tooling import (
    QRedTeaBackendLibraryImportError,
    assert_module_available,
    get_error_tensor_class,
)

# All modules have an __all__ defined
try:
    from .qteatorchtensor import *
except QRedTeaBackendLibraryImportError:
    # All the classes/functions are overwritten with a function that simply
    # raises an error when called
    assert_torch_available = partial(assert_module_available, module="torch")
    QteaTorchTensor = get_error_tensor_class(assert_torch_available)
    default_pytorch_backend = assert_torch_available
    default_abelian_pytorch_backend = assert_torch_available
    set_block_size_qteatorchtensors = assert_torch_available
    get_gpu_available = assert_torch_available
    DataMoverPytorch = assert_torch_available
