# -*- coding: utf-8 -*-

import json

from . import ATTRIBUTE_SPECIFICATION_PATH, REF_SPECIFICATION_PATH


class _OutputSpecification(object):

    def __init__(
            self, attribute_specification_path=ATTRIBUTE_SPECIFICATION_PATH,
            ref_specification_path=REF_SPECIFICATION_PATH
    ):
        self.attribute_specification_path = attribute_specification_path
        self.ref_specification_path = ref_specification_path

    @property
    def attribute_specification(self):
        with open(self.attribute_specification_path) as f:
            data = json.load(f)
        return data

    @property
    def ref_specification(self):
        with open(self.ref_specification_path) as f:
            data = json.load(f)
        return data

    def get_refs(self, resource_type):
        return self.ref_specification.get(resource_type, [])

    def get_attributes(self, resource_type):
        return self.attribute_specification.get(resource_type, [])
