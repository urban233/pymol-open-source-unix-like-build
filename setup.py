"""
#A* -------------------------------------------------------------------
#B* This file contains source code for building the python package of
#-* the PyMOL computer program
#C* Copyright 2025 by Martin Urban.
#D* -------------------------------------------------------------------
#E* It is unlawful to modify or remove this copyright notice.
#F* -------------------------------------------------------------------
#G* Please see the accompanying LICENSE file for further information.
#H* -------------------------------------------------------------------
#I* Additional authors of this source file include:
#-*
#-*
#-*
#Z* -------------------------------------------------------------------
"""
import pathlib
from setuptools import find_packages
from setuptools import setup
import toml

pyproject_toml = toml.load("pyproject.toml")
PROJECT_NAME = pyproject_toml["project"]["name"]
PROJECT_VERSION = pyproject_toml["project"]["version"]

PROJECT_ROOT_DIR = pathlib.Path(__file__).parent

# IMPORTANT: The MANIFEST.in is needed for the data folder!
setup(
  name=PROJECT_NAME,  # Name of your package
  version=PROJECT_VERSION,
  packages=find_packages(where='pymol'),  # Looks for packages in src/python
  package_dir={'': 'pymol'},  # src/python as the root for packages
  package_data={"": ["*.*"], "pymol": ["*.*"]},
  ext_modules=[],
  install_requires=[
    "numpy==1.26.4",
    "toml"
  ]
)
