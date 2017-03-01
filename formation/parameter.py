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

    def __eq__(self, other):
        # HACK: This method to allow us to compare generated
        # parameters to their expexted values in unit tests. It may have
        # unintended consequences..
        try:
            return all((
                self.title == other.title,
                self.param_type == other.param_type,
                self.default == other.default,
                self.allowed_values == other.allowed_values,
                self.description == other.description
            ))
        except AttributeError:
            return False

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
