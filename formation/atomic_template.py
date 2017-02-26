# -*- coding: utf-8 -*-

"""
formation.atomic_template implements the AtomicTemplate class.

"""

import json

import yaml

from .exception import InvalidPropertyError
from .output_specification import _OutputSpecification
from .resource_specification import _ResourceSpecification
from .parameter import Parameter


class AtomicTemplate(object):

    """
    A template containing a single resource, its parameters and outputs.

    Atomic templates are the smallest unit within Formation, and they can be
    merged together to form more complex templates.

    :param name: The name given to the resource.
    :type name: str
    :param resource_type: The AWS resource type, without the ``AWS::`` prefix.
        e.g. ``EC2::VPC`` or ``Lambda::Function``
    :type resource_type: str
    :param properties: A dict of properties to supply the resource.
    :type properties: dict

    """

    def __init__(self, name, resource_type, properties=None):
        self.name = name
        self.resource_type = "::".join(["AWS", resource_type])
        properties = {} if properties is None else properties
        _validate_properties(self._required_properties, properties)
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
        output_specification = _OutputSpecification()
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
    def _parameters(self):
        parameters = _get_parameters(self.properties)
        namespaced_parameters = {
            self._namespace(key): value
            for key, value in parameters.items()
        }
        return namespaced_parameters

    @property
    def _required_properties(self):
        resource_specification = _ResourceSpecification()
        return resource_specification.get_required_properties(
            self.resource_type
        )

    def _resolve_parameterised_properties(self, obj):
        """
        Recurses through the property dict and replaces ``Parameter`` objects
        with a Ref to that parameter's title.

        """
        if isinstance(obj, Parameter):
            return {"Ref": self._namespace(obj.title)}
        if isinstance(obj, dict):
            return {
                key: self._resolve_parameterised_properties(value)
                for key, value in obj.items()
            }
        if isinstance(obj, list):
            return [
                self._resolve_parameterised_properties(item)
                for item in obj
            ]
        return obj

    @property
    def _resources(self):
        """
        Returns the template's resources.

        """
        return {
            self.name: {
                "Type": self.resource_type,
                "Properties":
                    self._resolve_parameterised_properties(self.properties)
            }
        }

    @property
    def _template(self):
        """
        Returns the template.

        """
        template = {
            "Parameters": self._parameters,
            "Resources": self._resources,
            "Outputs": self._outputs
        }
        return template


def _validate_properties(required_properties, properties):
    """
    Raises an exception if required resource properties are not supplied.
    """
    required_resource_properties = [
        name
        for name, value in required_properties.items()
        if "Type" in value
    ]
    for required_resource_property in required_resource_properties:
        if required_resource_property not in properties:
            raise InvalidPropertyError(
                "The parameter '{0}' cannot be auto-assigned to a "
                "Parameter.".format(required_resource_property)
            )


def _get_properties(required_properties, properties):
    """
    """
    properties = {
        prop: Parameter(title=prop)
        for prop in required_properties
    }
    properties.update(properties)
    return properties


def _get_parameters(obj):
    """
    Returns a dict of the parameter templates, keyed by their titles.

    Recurses through a dictionary searching for
    ``formation.parameter.Parameter``s.
    """
    parameters = {}
    if isinstance(obj, Parameter):
        parameters[obj.title] = obj.template
    if isinstance(obj, dict):
        for value in obj.values():
            parameters.update(_get_parameters(value))
    if isinstance(obj, list):
        for item in obj:
            parameters.update(_get_parameters(item))
    return parameters
