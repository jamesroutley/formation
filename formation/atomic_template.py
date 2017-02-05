# -*- coding: utf-8 -*-

import json
import os

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
            "Parameters": self.parameters(),
            "Resources": self.resources()
        }
        return json.dumps(
            t, indent=indent, sort_keys=sort_keys, separators=separators
        )

    @property
    def _parameters(self):
        properties = get_properties(
            self.name, self.required_properties, self.properties
        )
        parameters = get_parameters(self.name, properties)
        return parameters

    @property
    def _resources(self, temp_name=None):
        name = temp_name if temp_name else self.name
        properties = get_properties(
            name, self.required_properties, self.properties
        )
        resource = get_resource(name, self.resource_type, properties)
        return resource


def get_properties(name, required_properties, user_properties):
    properties = {
        prop: Parameter()
        for prop in required_properties
    }
    properties.update(user_properties)
    return properties


def get_parameters(resource_name, properties):
    parameterised_properties = {
        prop_name: prop_value
        for prop_name, prop_value in properties.items()
        if isinstance(prop_value, Parameter)
    }
    parameters = {
        "".join([resource_name, prop_name]): {
            "Type": prop_value.param_type
        }
        for prop_name, prop_value in parameterised_properties.items()
    }
    # import ipdb; ipdb.set_trace()
    return parameters


def get_resource(name, resource_type, properties):
    # Maybe roll this into a couple of dict comps?
    for prop_name, prop_value in properties.items():
        if isinstance(prop_value, Parameter):
            # TODO: changing the thing we're iterating over seems dangerous
            # TODO: Change Ref to that ref function
            properties[prop_name] = {"Ref": "".join([name, prop_name])}
    return {
        name: {
            "Type": resource_type,
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
