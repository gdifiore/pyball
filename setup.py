#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyball",
    version="1.0.1",
    author="gdifiore",
    author_email="difioregabe@gmail.com",
    description="Python3 library for obtaining baseball information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gdifiore/pyball",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)