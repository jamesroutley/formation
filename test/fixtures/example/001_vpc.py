# -*- coding: utf-8 -*-

from __future__ import print_function

import os

from formation import AtomicTemplate


OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "output",
    "001_vpc.json"
)


def main():
    vpc = AtomicTemplate("VPC", "EC2::VPC")
    return vpc.to_json()


if __name__ == "__main__":
    print(main())
