#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qmetry-pytest",
    version="1.0.1",
    author="Prashanth Sams",
    author_email="sams.prashanth@gmail.com",
    maintainer="Prashanth Sams",
    maintainer_email="sams.prashanth@gmail.com",
    license="MIT",
    url="https://github.com/prashanth-sams/qmetry-pytest",
    description="A PyTest plugin that provides seamless integration with QMetry Test Management Platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["qmetry", "qmetry pytest", "reporter", "report", "pytest", "py.test", "jira", "cucumber", "xml"],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=["pytest", "requests"],
    classifiers=[
        "Framework :: Pytest",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "pytest11": [
            "qmetry = qmetry_pytest.plugin:QMetryPytestPlugin",
        ],
    }
)