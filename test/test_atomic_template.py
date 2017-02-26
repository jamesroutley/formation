# -*- coding: utf-8 -*-

import pytest

from formation.parameter import Parameter
import formation.atomic_template


@pytest.mark.parametrize("test_input,expected_output", [
    # Flat dict of parameters.
    (
        {"a": Parameter("a"), "b": Parameter("b"), "c": "c"},
        {"a": {"Type": "String"}, "b": {"Type": "String"}}
    ),
    # List of parameters
    (
        {"a": [Parameter("b"), Parameter("c")]},
        {"b": {"Type": "String"}, "c": {"Type": "String"}}
    ),
    # Nested dict of parameters
    (
        {"a": {"b": Parameter("b"), "c": Parameter("c")}},
        {"b": {"Type": "String"}, "c": {"Type": "String"}}
    ),
    # Nested list and dict
    (
        {"a": {"b": [Parameter("c")], "d": {"e": Parameter("e")}}},
        {"c": {"Type": "String"}, "e": {"Type": "String"}}
    )
])
def test_get_parameters(test_input, expected_output):
    output = formation.atomic_template._get_parameters(test_input)
    assert output == expected_output
