# -*- coding: utf-8 -*-

"""
formation.output_specification does not contain anything public.

"""

import json
import os


REF_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data", "refs.json"
)



class _OutputSpecification(object):

    def __init__(self, ref_specification_path=REF_SPECIFICATION_PATH):
        self.ref_specification_path = ref_specification_path

    @property
    def ref_specification(self):
        with open(self.ref_specification_path) as f:
            data = json.load(f)
        return data

    def get_refs(self, resource_type):
        return self.ref_specification.get(resource_type, [])
