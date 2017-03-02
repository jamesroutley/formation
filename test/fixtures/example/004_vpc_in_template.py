# -*- coding: utf-8 -*-

from __future__ import print_function

import os

from formation import AtomicTemplate, Template


OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "output",
    "004_vpc_in_template.yaml"
)


def main():
    template = Template()
    vpc = AtomicTemplate("VPC", "EC2::VPC")
    template.merge(vpc)
    return template.to_yaml()


if __name__ == "__main__":
    print(main())
