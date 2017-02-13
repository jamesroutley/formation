# -*- coding: utf-8 -*-

import json

import yaml

from . import ref
from .resource_specification import ResourceSpecification
from parameter import Parameter


class AtomicTemplate(object):

    def __init__(self, name, resource_type, properties=None):
        self.name = name
        self.resource_type = "::".join(["AWS", resource_type])
        self.properties = {} if properties is None else properties

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
            for prop in self._required_properties
        }
        properties.update(self.properties)
        return properties

    @property
    def _required_properties(self):
        resource_specification = ResourceSpecification()
        return resource_specification.get_required_properties(
            self.resource_type
        )

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
