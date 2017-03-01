# -*- coding: utf-8 -*-

"""
formation.resource_specification does not contain anything public.

"""

import json
import os


RESOURCE_SPECIFICATION_PATH = os.path.join(
    os.path.dirname(__file__), "data",
    "CloudFormationResourceSpecification.json"
)


class _ResourceSpecification(object):

    def __init__(
            self, resource_specification_path=RESOURCE_SPECIFICATION_PATH
    ):
        self.resource_specification_path = resource_specification_path

    def get_attributes(self, resource_type):
        resource_data = \
            self.resource_specification["ResourceTypes"][resource_type]
        return resource_data.get("Attributes", {})

    def get_required_properties(self, resource_type):
        resource_data = \
            self.resource_specification["ResourceTypes"][resource_type]
        required_properties = {
            prop_name: prop_details
            for prop_name, prop_details in resource_data["Properties"].items()
            if prop_details["Required"]
        }
        return required_properties

    @property
    def resource_specification(self):
        with open(self.resource_specification_path) as f:
            data = json.load(f)
        return data
