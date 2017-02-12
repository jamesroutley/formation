# -*- coding: utf-8 -*-

import json
import os

import yaml

from . import ref
from parameter import Parameter


class AtomicTemplate(object):

    def __init__(self, name, resource_type, properties=None):
        self.name = name
        self.resource_type = "::".join(["AWS", resource_type])
        self.properties = {} if properties is None else properties

        data_file_path = os.path.join(
            os.path.dirname(__file__), "data", "resource-specification.json"
        )
        with open(data_file_path) as f:
            data = json.load(f)
        resource_data = data["ResourceTypes"][self.resource_type]
        self.required_properties = get_required_properties(resource_data)

    def __repr__(self):
        return "AtomicTemplate({0})".format(self.name)

    def to_json(self, indent=4, sort_keys=True, separators=(',', ': ')):
        t = {
            "Parameters": self._parameters,
            "Resources": self._resources
        }
        return json.dumps(
            t, indent=indent, sort_keys=sort_keys, separators=separators
        )

    def to_yaml(self, default_flow_style=False):
        t = {
            "Parameters": self._parameters,
            "Resources": self._resources
        }
        return yaml.safe_dump(t, default_flow_style=default_flow_style)

    @property
    def _parameterised_properties(self):
        return {
            prop_name: prop_value
            for prop_name, prop_value in self._properties.items()
            if isinstance(prop_value, Parameter)
        }

    @property
    def _parameters(self):
        return {
            "".join([self.name, prop_name]): prop_value.get_representation()
            for prop_name, prop_value in self._parameterised_properties.items()
        }

    @property
    def _properties(self):
        properties = {
            prop: Parameter()
            for prop in self.required_properties
        }
        properties.update(self.properties)
        return properties

    @property
    def _resources(self):
        properties = self._properties
        properties.update({
            prop_name: ref("".join([self.name, prop_name]))
            for prop_name in self._parameterised_properties
        })
        return {
            self.name: {
                "Type": self.resource_type,
                "Properties": properties
            }
        }


def get_required_properties(resource_data):
    required_properties = [
        prop_name
        for prop_name, prop_details in resource_data["Properties"].items()
        if prop_details["Required"]
    ]
    return required_properties
