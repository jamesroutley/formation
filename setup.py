#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="formation",
    version="0.1.0",
    author="James Routley",
    author_email="jroutley@gmail.com",
    license="Apache2",
    packages=[
        "formation"
    ],
    package_dir={
        "formation": "formation"
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="test"
)
