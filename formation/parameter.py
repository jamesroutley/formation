# -*- coding: utf-8 -*-


class Parameter(object):

    def __init__(
            self, title, param_type="String", default=None,
            allowed_values=None, description=None
    ):
        self.title = title
        self.param_type = param_type
        self.default = default
        self.allowed_values = allowed_values
        self.description = description

    def __repr__(self):
        return (
            "formation.parameter.Parameter(title={0}, param_type={1})".format(
                self.title,
                self.param_type
            )
        )

    @property
    def template(self):
        """
        Returns a dict representation of the parameter.
        """
        representation = {
            "Type": self.param_type,
            "Default": self.default,
            "AllowedValues": self.allowed_values,
            "Description": self.description
        }
        representation = {
            k: v for k, v in representation.items() if v is not None
        }
        return representation
