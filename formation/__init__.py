# -*- coding: utf-8 -*-

import os


__version__ = "0.1.0"


RESOURCE_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data",
    "CloudFormationResourceSpecification.json"
)

ATTRIBUTE_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data", "get-atts.json"
)

REF_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data", "refs.json"
)
