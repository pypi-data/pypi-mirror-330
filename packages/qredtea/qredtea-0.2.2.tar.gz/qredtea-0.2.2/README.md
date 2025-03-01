[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

qredtea
=======

The quantum red tea library of Quantum TEA provides tensor beyond the dense
tensor with numpy or cupy, which could be either tensor for systems with
symmetries or tensor using another backend, e.g., pytorch.

Documentation
=============

[Here](https://quantum_red_tea.baltig-pages.infn.it/py_api_quantum_red_tea/)
is the documentation. The documentation can also be built locally via sphinx.

Backends
========

We list here the supported backends with the tested version:

* `pytorch==2.5.1`
* `jax==0.4.38`
* `tensorflow==2.18.0`

The version allow to install all four tensor backends (numpy, torch, jax, tensorflow)
within python3.11 environment (for CPUs).

License
=======

The project `qredtea` is hosted at the repository
``https://baltig.infn.it/quantum_red_tea/py_api_quantum_red_tea.git``,
and is licensed under the following license:

[Apache License 2.0](LICENSE)

The license applies to the files of this project as indicated
in the header of each file, but not its dependencies.


Installation
============

The `qredtea` library is never used as stand-alone package; it replaces
the tensor backend for one of the quantum TEA applications in agreement
with a `qtealeaves` version. Therefore, the minimal use-case to explore
the library is together with `qtealeaves`. Moreover, it can be used as
well with `qmatchatea`.

Local installation via pip
--------------------------

The package is available via a local pip installation as `pip install .`,
i.e., after cloning the repository.

Dependencies
------------

The python dependencies can be found in the [``requirements.txt``](requirements.txt)
and are required independently of the following use-cases.

Depending on your use-case, more requirements might be necessary at runtime. As
we implement the API to other packages via `qredtea`, we do not require the user
to install all of them.

qtealeaves simulations
----------------------

If you want to use the `qtealeaves` toolchain, a compatible version of 
`qtealeaves` has to be installed. The correct version is fetched
automatically if this package is installed via pip. Otherwise, see
[``requirements.txt``](requirements.txt).

qmatchatea simulations
----------------------

Quantum circuit simulations via `qmatchatea` require both `qredtea` and `qtealeaves`
as a dependency. Follow the instructions contained in the `qmatchatea` repository.
