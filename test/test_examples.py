# -*- coding: utf-8 -*-

"""
This module implements Formation's integration tests.

To add a new test case:
- Add a Python module containing a Formation template to ``fixtures/example``
- The module name should follow the naming convention
    ``<test number>_<description>.py``
- The module should implement a function ``main``, which returns the
    CloudFormation template encoded as a JSON string.
- A JSON file containing the expected output should be added to
    ``fixtures/output``
- The expected output file should have the same name as the example, but with
    a ``.json`` extension. e.g. ``<test number>_<description>.json``.

"""

import glob
import imp
import os

import yaml

import pytest


EXAMPLE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "fixtures", "example"
))


def _get_examples():
    """
    Returns all .py files found in EXAMPLE_DIR.
    """
    pattern = os.path.join(EXAMPLE_DIR, "*.py")
    return glob.glob(pattern)


def _read_file(path):
    """
    Returns the contents of the file at ``path``.

    """
    with open(path) as f:
        expected_output = f.read()
    return expected_output


@pytest.mark.parametrize("example_file", _get_examples())
def test_example_formation_compiles_to_expected_json(example_file):
    """
    Compiles the Formation code in each example file and compares it to
    expected output.

    """
    name = os.path.basename(example_file).split(".")[0]
    module = imp.load_source(name, example_file)
    actual_output = module.main()
    expected_output = _read_file(module.OUTPUT_FILE)
    assert yaml.safe_load(actual_output) == yaml.safe_load(expected_output)
