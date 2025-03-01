# This code is part of qredtea.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import importlib.util
import os.path

import setuptools

# Parse the version file
spec = importlib.util.spec_from_file_location("qredtea", "./qredtea/version.py")
version_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version_module)

# Get the readme file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define requirements
install_requires = [
    "numpy",
    "scipy",
    "matplotlib",
    "mpmath",
    "joblib",
    "h5py",
    "qtealeaves>=1.5.8,<1.6.0",
]
# only for developers
# "sphinx",
# "sphinx-gallery",
# "sphinx_rtd_theme",
# "pre-commit",

setuptools.setup(
    name="qredtea",
    version=version_module.__version__,
    author=", ".join(
        [
            "Francesco Pio Barone",
            "Flavio Baccari",
            "Marco Ballarin",
            "Alberto Coppi",
            "Andrea De Girolamo",
            "Daniel Jaschke",
            "Luka Pavešić",
            "Davide Rattacaso",
            "Nora Reinić",
            "Carmelo Mordini",
        ]
    ),
    author_email="quantumtea@lists.infn.it",
    description="Quantum TEA's python tensor library beyond numpy/cupy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://baltig.infn.it/quantum_red_tea/py_api_quantum_red_tea.git",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={
        "qredtea": "qredtea",
        "qredtea.symmetries": "qredtea/symmetries",
        "qredtea.tooling": "qredtea/tooling",
        "qredtea.torchapi": "qredtea/torchapi",
        "qredtea.jaxapi": "qredtea/jaxapi",
        "qredtea.tensorflowapi": "qredtea/tensorflowapi",
    },
    packages=[
        "qredtea",
        "qredtea.symmetries",
        "qredtea.tooling",
        "qredtea.torchapi",
        "qredtea.jaxapi",
        "qredtea.tensorflowapi",
    ],
    python_requires=">=3.11",
    install_requires=install_requires,
)
