# -*- coding: utf-8 -*-

from formation.atomic_template import AtomicTemplate


def main():
    vpc = AtomicTemplate("VPC", "EC2::VPC")
    return vpc.to_json()


if __name__ == "__main__":
    print main()