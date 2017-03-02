# -*- coding: utf-8 -*-

"""
formation.parameter implements the Parameter class.

"""


OPTIONAL_PROPERTIES = [
    "allowed_pattern",
    "allowed_values",
    "constraint_description",
    "default",
    "description",
    "max_length",
    "max_value",
    "min_length",
    "min_value",
    "no_echo"
]


class Parameter(object):

    """
    A CloudFormation template parameter.

    """

    def __init__(self, title, param_type="String", **kwargs):
        self.title = title
        self.param_type = param_type
        self.optional_properties = kwargs
        _validate_kwargs(kwargs.keys())

    def __repr__(self):
        """
        Returns a string representation of the object.

        :returns: A string representation of the object.
        :rtype: self

        """
        return (
            "formation.parameter.Parameter(title='{0}', param_type='{1}', "
            "**{2})".format(
                self.title, self.param_type, self.optional_properties
            )
        )

    def __eq__(self, other):
        """
        Returns True if self == other else False.

        :param other: An object to compare equality with.
        :type other: obj
        :returns: A boolean representing whether self == other.
        :rtype: bool

        """
        # HACK: This method to allow us to compare generated
        # parameters to their expexted values in unit tests. It may have
        # unintended consequences..
        try:
            return all((
                self.title == other.title,
                self.optional_properties == other.optional_properties
            ))
        except AttributeError:
            return False

    @property
    def template(self):
        """
        Returns a the parameter as it appears in CloudFormation as a dict.

        :returns: A dictionary representation of the parameter.
        :rtype: dict

        """
        representation = {"Type": self.param_type}
        representation.update({
            _snake_to_camel(key): value
            for key, value in self.optional_properties.items()
        })
        return representation


def _snake_to_camel(snake_case_string):
    """
    Returns a CamelCase version of the snake_case input string.

    :param snake_case_string: A string in snake_case.
    :type snake_case_string: str

    """
    words = snake_case_string.split("_")
    return "".join((word.capitalize() for word in words))


def _validate_kwargs(keyword_arguments):
    """
    Raises a TypeError if an argument is not in
        formation.parameter.OPTIONAL_PROPERTIES.

    :param keyword_arguments: A list of keyword argument names to validate.
    :type keyword_arguments: list
    :raises: TypeError

    """
    for argument in keyword_arguments:
        if argument not in OPTIONAL_PROPERTIES:
            raise TypeError(
                "__init__() got an unexpected keyword argument "
                "'{0}'".format(argument)
            )
