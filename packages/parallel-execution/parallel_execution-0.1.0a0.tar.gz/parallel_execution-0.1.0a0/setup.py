# -- import packages: ---------------------------------------------------------
import setuptools
import re
import os
import sys


# -- define variables: --------------------------------------------------------
NAME: str = "parallel_execution"
DESCRIPTION: str = "parallel execution in python; multithreading"


# -- fetch specification files: -----------------------------------------------
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open(f'{NAME}/__version__.py') as v:
    exec(v.read())


# -- run setup: ---------------------------------------------------------------
setuptools.setup(
    name=NAME,
    version=__version__,
    python_requires=">3.9.0",
    author="Michael E. Vinyard",
    author_email="mvinyard.ai@gmail.com",
    url="https://github.com/QuintessenceLabs",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description=DESCRIPTION,
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
