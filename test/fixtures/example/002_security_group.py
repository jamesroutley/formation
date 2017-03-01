# -*- coding: utf-8 -*-

from formation import AtomicTemplate, Parameter


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
    print main()
