# -*- coding: utf-8 -*-

from __future__ import print_function

import os

from formation import AtomicTemplate, Parameter


OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "output",
    "002_security_group.json"
)


def main():
    ingress_cidr_blocks = ["10.0.0.0/24", "169.125.0.0/24"]
    sg = AtomicTemplate(
        "SecurityGroup",
        "EC2::SecurityGroup",
        properties={
            "GroupDescription": "my security group",
            "VpcId": Parameter("VpcId"),
            "SecurityGroupIngress": [
                {
                    "CidrIp": cidr_block,
                    "FromPort": "80",
                    "ToPort": "80"
                }
                for cidr_block in ingress_cidr_blocks
            ]
        }
    )
    return sg.to_json()


if __name__ == "__main__":
    print(main())
