#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

# Package meta-data.
AUTHOR = "Gertjan van den Burg"
DESCRIPTION = "A command line tool for easily managing benchmark experiments"
EMAIL = "gertjanvandenburg@gmail.com"
LICENSE = "GPLv2"
LICENSE_TROVE = "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
NAME = "abed"
REQUIRES_PYTHON = ">=3.4.0"
URL = "https://github.com/GjjvdBurg/abed"
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    "Fabric3==1.14.post1",
    "backports.lzma",
    "bz2file",
    "colorama",
    "dominate",
    "gitpython",
    "mpi4py",
    "progressbar",
    "python-dateutil",
    "scipy",
    "six",
    "tabulate",
    "tqdm",
]

docs_require = []
test_require = []
dev_require = []

# What packages are optional?
EXTRAS = {
    "docs": docs_require,
    "tests": test_require,
    "dev": docs_require + test_require + dev_require,
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))


def get_data_files():
    datadir = os.path.join("share", "data")
    datafiles = []
    for root, dirs, files in os.walk(datadir):
        if not dirs:
            newfiles = [os.path.join(root, f) for f in files]
            datafiles.append((root, newfiles))
    return datafiles


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    data_files=get_data_files(),
    # include_package_data=True,
    license=LICENSE,
    ext_modules=[],
    scripts=["bin/abed"],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        LICENSE_TROVE,
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
)
