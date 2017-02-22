# -*- coding: utf-8 -*-

import json

from . import RESOURCE_SPECIFICATION_PATH


class _ResourceSpecification(object):

    def __init__(
            self, resource_specification_path=RESOURCE_SPECIFICATION_PATH
    ):
        self.resource_specification_path = resource_specification_path

    @property
    def resource_specification(self):
        with open(self.resource_specification_path) as f:
            data = json.load(f)
        return data

    def get_required_properties(self, resource_type):
        resource_data = \
            self.resource_specification["ResourceTypes"][resource_type]
        required_properties = [
            prop_name
            for prop_name, prop_details in resource_data["Properties"].items()
            if prop_details["Required"]
        ]
        return required_properties
