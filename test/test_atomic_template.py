# -*- coding: utf-8 -*-

import pytest

import formation.atomic_template
from formation.exception import InvalidPropertyError
from formation.parameter import Parameter


@pytest.mark.parametrize(
    "required_properties,user_properties,expected_output",
    [
        (
            {
                "Code": {
                    "Documentation": "<truncated>",
                    "Required": True,
                    "PrimitiveType": "String",
                    "UpdateType": "Immutable"
                }
            },
            {},
            None
        ),
        (
            {
                "Code": {
                    "Documentation": "<truncated>",
                    "Required": True,
                    "Type": "Code",
                    "UpdateType": "Mutable"
                }
            },
            {},
            InvalidPropertyError
        )
    ]
)
def test_validate_properties(
        required_properties, user_properties, expected_output
):
    if expected_output and issubclass(expected_output, Exception):
        with pytest.raises(expected_output):
            formation.atomic_template._validate_properties(
                required_properties, user_properties
            )
    else:
        output = formation.atomic_template._validate_properties(
            required_properties, user_properties
        )
        assert output == expected_output


@pytest.mark.parametrize(
    "required_properties,user_properties,expected_output",
    [
        (
            ["CidrBlock"],
            {},
            {
                "CidrBlock": Parameter("CidrBlock")
            }
        ),
        (
            ["CidrBlock"],
            {"CidrBlock": "10.0.0.0/24"},
            {
                "CidrBlock": "10.0.0.0/24"
            }
        ),
        (
            ["CidrBlock"],
            {"EnableDnsSupport": False},
            {
                "CidrBlock": Parameter("CidrBlock"),
                "EnableDnsSupport": False
            }
        ),
        (
            ["CidrBlock"],
            {"EnableDnsSupport": Parameter("MyEnableDnsSupportParam")},
            {
                "CidrBlock": Parameter("CidrBlock"),
                "EnableDnsSupport": Parameter("MyEnableDnsSupportParam")
            }
        ),
        (
            ["CidrBlock"],
            {"Tags": [{"Key": "Name", "Value": Parameter("VpcName")}]},
            {
                "CidrBlock": Parameter("CidrBlock"),
                "Tags": [{"Key": "Name", "Value": Parameter("VpcName")}]
            }
        ),
    ]
)
def test_get_properties(required_properties, user_properties, expected_output):
    output = formation.atomic_template._get_properties(
        required_properties,
        user_properties
    )
    assert output == expected_output


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
