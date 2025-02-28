#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#  Copyright (c) 2025 Emanuele Ballarin <emanuele@ballarin.cc>
#  Released under the terms of the MIT License
#  (see: https://url.ballarin.cc/mitlicense)
#
# ------------------------------------------------------------------------------
import os

from setuptools import find_packages
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read().strip()


PACKAGENAME: str = "thrmt"

setup(
    name=PACKAGENAME,
    version="0.0.13",
    author="Emanuele Ballarin",
    author_email="emanuele@ballarin.cc",
    url="https://github.com/emaballarin/thrmt",
    description="Torched Random Matrix Theory",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords=[
        "Deep Learning",
        "Differentiable Programming",
        "Machine Learning",
        "PyTorch",
        "Random Matrices",
        "Random Matrix Theory",
    ],
    license="MIT",
    packages=[
        package for package in find_packages() if package.startswith(PACKAGENAME)
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
    install_requires=["torch>=2"],
    include_package_data=False,
    zip_safe=True,
)
