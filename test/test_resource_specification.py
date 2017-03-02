# -*- coding: utf-8 -*-

import os

import pytest

from formation.resource_specification import _ResourceSpecification


@pytest.fixture
def resource_specification():
    """
    Returns an initialised _ResourceSpecification.

    The resource specification document is stored at
    ``test/fixtures/specification/CloudFormationResourceSpecification.json``.
    We do not use the defualt document. If we did and it was updated, these
    tests may break even though the code still worked.

    """
    specification_path = os.path.join(
        os.path.dirname(__file__), "fixtures", "specification",
        "CloudFormationResourceSpecification.json"
    )
    resource_specification = _ResourceSpecification(
        resource_specification_path=specification_path
    )
    return resource_specification


def test_get_attributes(resource_specification):
    expected_output = {
        "CidrBlock": {
            "PrimitiveType": "String"
        },
        "DefaultNetworkAcl": {
            "PrimitiveType": "String"
        },
        "DefaultSecurityGroup": {
            "PrimitiveType": "String"
        },
        "Ipv6CidrBlocks": {
            "PrimitiveItemType": "String",
            "Type": "List"
        }
    }
    output = resource_specification.get_attributes("AWS::EC2::VPC")
    assert output == expected_output


def test_get_required_properties(resource_specification):
    expected_output = {
        "CidrBlock": {
            "Documentation":
                "http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide"
                "/aws-resource-ec2-vpc.html#cfn-aws-ec2-vpc-cidrblock",
            "PrimitiveType": "String",
            "Required": True,
            "UpdateType": "Immutable"
        }
    }
    output = resource_specification.get_required_properties("AWS::EC2::VPC")
    assert output == expected_output
