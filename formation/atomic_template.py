# -*- coding: utf-8 -*-

import json

import yaml

from . import ref
from .resource_specification import ResourceSpecification
from .parameter import Parameter


class AtomicTemplate(object):

    def __init__(self, name, resource_type, properties=None):
        self.name = name
        self.resource_type = "::".join(["AWS", resource_type])
        properties = {} if properties is None else properties
        self.properties = _get_properties(
            self._required_properties, properties
        )

    def __repr__(self):
        return "AtomicTemplate({0})".format(self.name)

    def to_json(self, indent=4, sort_keys=True, separators=(',', ': ')):
        return json.dumps(
            self._template, indent=indent,
            sort_keys=sort_keys, separators=separators
        )

    def to_yaml(self, default_flow_style=False):
        return yaml.safe_dump(
            self._template, default_flow_style=default_flow_style
        )

    def _namespace(self, string):
        """
        Prepends the resource name to string and returns the result.
        """
        return "".join([self.name, string])

    @property
    def _parameterised_properties(self):
        return {
            prop_name: prop_value
            for prop_name, prop_value in self.properties.items()
            if isinstance(prop_value, Parameter)
        }

    @property
    def _parameters(self):
        return {
            self._namespace(prop_name): prop_value.template
            for prop_name, prop_value in self._parameterised_properties.items()
        }

    @property
    def _required_properties(self):
        resource_specification = ResourceSpecification()
        return resource_specification.get_required_properties(
            self.resource_type
        )

    @property
    def _resources(self):
        properties = self.properties
        properties.update({
            prop_name: ref(self._namespace(prop_name))
            for prop_name in self._parameterised_properties
        })
        return {
            self.name: {
                "Type": self.resource_type,
                "Properties": properties
            }
        }

    @property
    def _template(self):
        template = {
            "Parameters": self._parameters,
            "Resources": self._resources
        }
        return template


def _get_properties(required_properties, user_properties):
    properties = {
        prop: Parameter()
        for prop in required_properties
    }
    properties.update(user_properties)
    return properties
