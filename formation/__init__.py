# -*- coding: utf-8 -*-


__version__ = "0.1.0"


def ref(data):
    return {"Ref": data}


def get_att(data, attribute):
    return {"Fn::GetAtt": [data, attribute]}
