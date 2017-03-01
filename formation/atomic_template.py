# -*- coding: utf-8 -*-

"""
formation.atomic_template implements the AtomicTemplate class.

"""

from .base_template import BaseTemplate
from .exception import InvalidPropertyError
# from .output_specification import _OutputSpecification
from .resource_specification import _ResourceSpecification
from .parameter import Parameter


class AtomicTemplate(BaseTemplate):

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

    def __init__(self, title, resource_type, properties=None):
        self.title = title
        self.resource_type = "::".join(["AWS", resource_type])
        properties = {} if properties is None else properties
        _validate_properties(self._required_properties, properties)
        self.properties = _get_properties(
            self._required_properties.keys(), properties
        )

    def __repr__(self):
        return "AtomicTemplate({0})".format(self.title)

    def _namespace(self, string):
        """
        Prepends the resource name to ``string`` and returns the result.

        :param string: A string to prepend the resource name to.
        :type string: str
        :returns: A string with the resource name prepended to it.
        :rtype: str

        """
        return "".join([self.title, string])

    @property
    def _outputs(self):
        # output_specification = _OutputSpecification()
        resource_specification = _ResourceSpecification()
        attributes = resource_specification.get_attributes(self.resource_type)
        outputs = {
            self._namespace(attribute): {
                "Value": {"Fn::GetAtt": [self.title, attribute]}
            }
            for attribute in attributes
        }
        # BUG: not all resources have a Ref value.
        outputs[self._namespace("Ref")] = {
            "Value": {"Ref": self.title}
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
            self.title: {
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
    Raises error if required resource-specific properties are not supplied.
    """
    required_resource_specific_properties = [
        name
        for name, value in required_properties.items()
        if "Type" in value
    ]
    for required_resource_property in required_resource_specific_properties:
        if required_resource_property not in properties:
            raise InvalidPropertyError(
                "The resource-specific parameter '{0}' cannot be auto-assigned"
                "to a Parameter.".format(required_resource_property)
            )


def _get_properties(required_properties, user_properties):
    """
    Returns the resource's properties.

    Adds a parameterised property for each required property not supplied by
    the user.

    :param required_properties: A list of required resource property names.
    :type required_properties: list
    :param user_properties: The properties supplied by the user.
    :type user_properties: dict
    :returns: The template's resource's properties.
    :rtype: dict

    """
    properties = {
        prop: Parameter(title=prop)
        for prop in required_properties
    }
    properties.update(user_properties)
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
