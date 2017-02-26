# -*- coding: utf-8 -*-

import os


__version__ = "0.1.0"


RESOURCE_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data",
    "CloudFormationResourceSpecification.json"
)

REF_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data", "refs.json"
)
