# -*- coding: utf-8 -*-

import os


__version__ = "0.1.0"


RESOURCE_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data", "resource-specification.json"
)


def ref(data):
    return {"Ref": data}


def get_att(data, attribute):
    return {"Fn::GetAtt": [data, attribute]}
