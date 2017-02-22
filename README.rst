=========
Formation
=========

.. warning::

  Formation is under active development and its API is unstable.

Formation defines a terse Python syntax which compiles to CloudFormation. Formation aims to automate the CloudFormation template writing process.


Motivation
----------

Formation aims to bring two new features to CloudFormation:

- automation
- composability


Automation
**********

Formation aggressively automates the CloudFormation template writing process. If we wish to create a CloudFormation template containing a VPC, we can write the following:

.. code-block:: yaml

  Resources:
    VPC:
      Type: AWS::EC2::VPC

VPCs require a `CIDR block <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html#cfn-aws-ec2-vpc-cidrblock>`_ property. We can specify the CIDR block of our VPC as ``10.0.0.0/16``:

.. code-block:: yaml

  Resources:
    VPC:
      Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16

However, it is considered bad practice to hardcode values in templates. We can improve reusability by moving the value of the CIDR block to a `Parameter <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html>`_. The person who uses the template can set the CIDR block value.

.. code-block:: yaml

  Parameters:
    CidrBlockParam:
      Type: String

  Resources:
    VPC:
      Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref CidrBlockParam

We should add relevant `Outputs <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html>`_ to our VPC stack. Outputs allow us to find out information about the resources contained in a stack. VPCs have the following outputs: ``VpcId``, ``CidrBlock``, ``DefaultNetworkAcl``, ``DefaultSecurityGroup`` and ``Ipv6CidrBlocks``. We should add them all, so we won't have to later if we happen to require one:

.. code-block:: yaml

  Outputs:
    VpcId:
      Value: !Ref VPC
    CidrBlock:
      Value: !GetAtt VPC.CidrBlock
    DefaultNetworkAcl:
      Value: !GetAtt VPC.DefaultNetworkAcl
    DefaultSecurityGroup:
      Value: !GetAtt VPC.DefaultSecurityGroup
    Ipv6CidrBlocks:
      Value: !GetAtt VPC.Ipv6CidrBlocks

  Parameters:
    CidrBlockParam:
      Type: String

  Resources:
    VPC:
      Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref CidrBlockParam

We see that creating a simple CloudFormation template containing a single VPC requires writing a lot of boilerplate code. Formation aims to automate this. Formation looks up a resource's required properties and automatically parameterises them. Formation looks up a resource's outputs and automatically adds them.

.. code-block:: python

  >>> from formation.atomic_template import AtomicTemplate
  >>> vpc = AtomicTemplate("VPC", "EC2::VPC")
  >>> print vpc.to_yaml()
  Outputs:
  VPCCidrBlock:
    Value:
      Fn::GetAtt:
      - VPC
      - CidrBlock
  VPCDefaultNetworkAcl:
    Value:
      Fn::GetAtt:
      - VPC
      - DefaultNetworkAcl
  VPCDefaultSecurityGroup:
    Value:
      Fn::GetAtt:
      - VPC
      - DefaultSecurityGroup
  VPCIpv6CidrBlocks:
    Value:
      Fn::GetAtt:
      - VPC
      - Ipv6CidrBlocks
  VPCRef:
    Value:
      Ref: VPC
  Parameters:
    VPCCidrBlock:
      Type: String
  Resources:
    VPC:
      Properties:
        CidrBlock:
          Ref: VPCCidrBlock
      Type: AWS::EC2::VPC

A few lines of Python produce functionally identical CloudFormation.


Composability
*************

TODO
