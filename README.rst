=========
Formation
=========

Warning: Formation is under active development and its API is unstable.

Formation defines a terse Python syntax which compiles to CloudFormation. Formation aims to bring two new features to CloudFormation:

- `Automation`_
- `Composability`_


Features
--------

Automation
**********

Formation aggressively automates the CloudFormation template writing process. To show this, we first examine a template written in stock CloudFormation. To create a template containing a VPC, we can write the following:

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

  >>> from formation import AtomicTemplate
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

Stock CloudFormation templates suffer from two problems:

- Complexity. As infrastructure is added, CloudFormation templates grow in size and complexity. Individual templates often become hundreds or thousands of lines long. This leads to templates that are difficult to understand. Systems which are difficult to understand are more error prone.
- Reusability. Sections of code are often repeated across CloudFormation templates. This is wasteful, and any changes need to be made in multiple places.

We can solve both these problems by modularising CloudFormation templates. Large templates can be broken down into smaller chunks, and reusable pieces of code can be refactored out. Modularity isn't natively supported in CloudFormation. Small, reusable templates can be written, but the only way to combine them is by copying and pasting their contents. Formation's composability gives you the power to write modular templates and combine them programatically.

.. code-block:: python

  >>> from formation import AtomicTemplate, Template

  >>> vpc = AtomicTemplate("VPC", "EC2::VPC")
  >>> subnet = AtomicTemplate("Subnet", "EC2::Subnet")
  >>> network = Template()
  >>> network.merge(vpc)
  >>> network.merge(subnet)
  >>> print network.to_yaml()
  Outputs:
    SubnetAvailabilityZone:
      Value:
        Fn::GetAtt:
        - Subnet
        - AvailabilityZone
    ...  # Output truncated
  Parameters:
    SubnetCidrBlock:
      Type: String
    SubnetVpcId:
      Type: String
    VPCCidrBlock:
      Type: String
  Resources:
    Subnet:
      Properties:
        CidrBlock:
          Ref: SubnetCidrBlock
        VpcId:
          Ref: SubnetVpcId
      Type: AWS::EC2::Subnet
    VPC:
      Properties:
        CidrBlock:
          Ref: VPCCidrBlock
      Type: AWS::EC2::VPC

In this example, two modularised templates, ``vpc`` and ``subnet`` are composed into a single ``network`` template.
