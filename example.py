# -*- coding: utf-8 -*-

from formation.template import Template
from formation.parameter import Parameter
from formation.atomic_template import AtomicTemplate


t = Template()
vpc = AtomicTemplate("MyVPC", "EC2::VPC", properties={
    "EnableDnsSupport": Parameter()
})
# subnet = AtomicTemplate("MySubnet", "EC2::Subnet")
t.merge(vpc)
# t.merge(subnet)

# t2 = Template()
# vpc2 = AtomicTemplate("MyVPC2", "EC2::VPC")
# subnet2 = AtomicTemplate("MySubnet", "EC2::Subnet")
# t2.merge(vpc2)
# t2.merge(subnet2)

# t.merge(t2)
print t.to_yaml()
