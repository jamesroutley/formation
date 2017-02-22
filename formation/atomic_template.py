# -*- coding: utf-8 -*-

import json

import yaml

# from . import get_att, ref
from .output_specification import OutputSpecification
from .resource_specification import ResourceSpecification
from .parameter import Parameter


class AtomicTemplate(object):

    """
    AtomicTemplate contains a single resource, and its parameters and outputs.

    :param name: The name given to the resource.
    :type name: str
    :param resource_type: The AWS resource type, without the "AWS::" prefix.
        e.g. "EC2::VPC" or "Lambda::Function"
    :type resource_type: str
    :param properties: A dict of properties to supply the resource.
    :type properties: dict

    """

    def __init__(self, name, resource_type, properties=None):
        self.name = name
        self.resource_type = "::".join(["AWS", resource_type])
        properties = {} if properties is None else properties
        self.properties = _get_properties(
            self._required_properties, properties
        )

    def __repr__(self):
        return "AtomicTemplate({0})".format(self.name)

    def to_json(
            self, indent=4, sort_keys=True, separators=(',', ': '),
            **json_dumps_kwargs
    ):
        """
        Returns the CloudFormation template as a JSON string.

        :param indent: The number of spaces to indent JSON by.
        :type indent: int
        :param sort_keys: Whether to sort keys or not.
        :type sort_keys: bool
        :param separators: A tuple of separators to use.
        :type separators: tuple
        :param json_dumps_kwargs: kwargs to pass on to ``json.dumps``.
        :type json_dumps_kwargs: kwargs
        :returns: The CloudFormation template encoded as JSON.
        :rtype: str

        """
        return json.dumps(
            self._template, indent=indent, sort_keys=sort_keys,
            separators=separators, **json_dumps_kwargs
        )

    def to_yaml(self, default_flow_style=False, **yaml_safe_dump_kwargs):
        """
        Returns the CloudFormation template as a YAML string.

        :param default_flow_style: Whether to serialize YAML in the block
            style.
        :type default_flow_style: bool
        :param yaml_safe_dump_kwargs: kwargs to pass on to ``yaml.safe_dump``.
        :type yaml_safe_dump_kwargs: kwargs
        :returns: The CloudFormation template encoded as YAML.
        :rtype: str

        """
        return yaml.safe_dump(
            self._template, default_flow_style=default_flow_style,
            **yaml_safe_dump_kwargs
        )

    def _namespace(self, string):
        """
        Prepends the resource name to ``string`` and returns the result.

        :param string: A string to prepend the resource name to.
        :type string: str
        :returns: A string with the resource name prepended to it.
        :rtype: str

        """
        return "".join([self.name, string])

    @property
    def _outputs(self):
        output_specification = OutputSpecification()
        attributes = output_specification.get_attributes(self.resource_type)
        outputs = {
            self._namespace(attribute["Attribute"]): {
                # "Description": attribute["Description"],
                "Value": {"Fn::GetAtt": [self.name, attribute["Attribute"]]}
            }
            for attribute in attributes
        }
        # refs = output_specification.get_refs(self.resource_type)
        outputs[self._namespace("Ref")] = {
            # "Description": refs["Reference Value"],
            "Value": {"Ref": self.name}
        }
        return outputs

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
            prop_name: {"Ref": self._namespace(prop_name)}
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
            "Resources": self._resources,
            "Outputs": self._outputs
        }
        return template


def _get_properties(required_properties, user_properties):
    properties = {
        prop: Parameter()
        for prop in required_properties
    }
    properties.update(user_properties)
    return properties
