# -*- coding: utf-8 -*-

import pytest

import formation.atomic_template
from formation.exception import InvalidPropertyError
from formation.parameter import Parameter


@pytest.mark.parametrize("properties,resource_title,expected_output", [
    # Flat dict of parameters.
    (
        {"A": Parameter("A"), "B": Parameter("B"), "C": "C"},
        "Title",
        {"TitleA": {"Type": "String"}, "TitleB": {"Type": "String"}}
    ),
    # List of parameters
    (
        {"A": [Parameter("B"), Parameter("C")]},
        "Title",
        {"TitleB": {"Type": "String"}, "TitleC": {"Type": "String"}}
    ),
    # Nested dict of parameters
    (
        {"A": {"B": Parameter("B"), "C": Parameter("C")}},
        "Title",
        {"TitleB": {"Type": "String"}, "TitleC": {"Type": "String"}}
    ),
    # Nested list and dict
    (
        {"A": {"B": [Parameter("C")], "D": {"E": Parameter("E")}}},
        "Title",
        {"TitleC": {"Type": "String"}, "TitleE": {"Type": "String"}}
    )
])
def test_get_parameters(properties, resource_title, expected_output):
    output = formation.atomic_template._get_parameters(
        properties, resource_title
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


@pytest.mark.parametrize("properties,resource_title,expected_output", [
    # Flat dict of parameters.
    (
        {"A": Parameter("A"), "B": Parameter("B"), "C": "C"},
        "Title",
        {"A": {"Ref": "TitleA"}, "B": {"Ref": "TitleB"}, "C": "C"}
    ),
    # List of parameters
    (
        {"A": [Parameter("B"), Parameter("C")]},
        "Title",
        {"A": [{"Ref": "TitleB"}, {"Ref": "TitleC"}]}
    ),
    # Nested dict of parameters
    (
        {"A": {"B": Parameter("B"), "C": Parameter("C")}},
        "Title",
        {"A": {"B": {"Ref": "TitleB"}, "C": {"Ref": "TitleC"}}}
    ),
    # Nested list and dict
    (
        {"A": {"B": [Parameter("C")], "D": {"E": Parameter("E")}}},
        "Title",
        {"A": {"B": [{"Ref": "TitleC"}], "D": {"E": {"Ref": "TitleE"}}}}
    )
])
def test_resolve_parameterised_properties(
        properties, resource_title, expected_output
):
    output = formation.atomic_template._resolve_parameterised_properties(
        properties, resource_title
    )
    assert output == expected_output


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
