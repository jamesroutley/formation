# -*- coding: utf-8 -*-

import pytest

import formation.parameter
from formation.parameter import Parameter


@pytest.mark.parametrize("parameter,expected_output", [
    (
        Parameter("A"),
        "formation.parameter.Parameter(title='A', param_type='String', **{})"
    ),
    (
        Parameter("A", "Number"),
        "formation.parameter.Parameter(title='A', param_type='Number', **{})"
    ),
    (
        Parameter("A", "Number", description="My description"),
        "formation.parameter.Parameter(title='A', param_type='Number', "
        "**{'description': 'My description'})"
    ),
    (
        Parameter("A", "Number", description="My description"),
        "formation.parameter.Parameter(title='A', param_type='Number', "
        "**{'description': 'My description'})"
    )
])
def test_repr(parameter, expected_output):
    assert parameter.__repr__() == expected_output


@pytest.mark.parametrize("left,right,output", [
    (Parameter("A"), Parameter("A"), True),
    (Parameter("A"), Parameter("B"), False),
    (Parameter("A"), 1, False),
    (Parameter("A", default="a"), Parameter("A", default="a"), True)
])
def test_eq(left, right, output):
    assert (left == right) == output


@pytest.mark.parametrize("snake,camel", [
    ("", ""),
    ("my_words", "MyWords"),
    ("word_1", "Word1"),
    (" ", " "),
    ("1_word", "1Word")
])
def test_snake_to_camel(snake, camel):
    output = formation.parameter._snake_to_camel(snake)
    assert output == camel


def test_validate_kwargs_with_expected_keywords():
    allowed_properties = [
        "allowed_pattern",
        "allowed_values",
        "constraint_description",
        "default",
        "description",
        "max_length",
        "max_value",
        "min_length",
        "min_value",
        "no_echo"
    ]
    kwargs = {
        property_name: "mock_value"
        for property_name in allowed_properties
    }
    formation.parameter._validate_kwargs(kwargs)


def test_validate_kwargs_with_unexpected_keyword():
    kwargs = {"unexpected_keyword": "mock_value"}
    with pytest.raises(TypeError):
        formation.parameter._validate_kwargs(kwargs)
