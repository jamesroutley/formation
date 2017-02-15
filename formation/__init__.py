# -*- coding: utf-8 -*-

import os


__version__ = "0.1.0"


RESOURCE_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data", "resource-specification.json"
)

ATTRIBUTE_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data", "get-atts.json"
)

REF_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data", "refs.json"
)


def ref(data):
    return {"Ref": data}


def get_att(data, attribute):
    return {"Fn::GetAtt": [data, attribute]}
