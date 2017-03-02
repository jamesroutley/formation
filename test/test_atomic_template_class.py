# -*- coding: utf-8 -*-

import pytest

from formation.atomic_template import AtomicTemplate


@pytest.mark.parametrize("atomic_template,expected_output", [
    (
        AtomicTemplate("VPC", "EC2::VPC"),
        "AtomicTemplate(title='VPC', resource_type='EC2::VPC', "
        "properties={})"
    ),
    (
        AtomicTemplate("VPC", "EC2::VPC", {"EnableDnsHostnames": True}),
        "AtomicTemplate(title='VPC', resource_type='EC2::VPC', "
        "properties={'EnableDnsHostnames': True})"
    )
])
def test_repr(atomic_template, expected_output):
    output = atomic_template.__repr__()
    assert output == expected_output
