# -*- coding: utf-8 -*-

"""
formation.exception implements the exceptions raised by Formation.

"""


class FormationError(Exception):
    """
    Formation's base exception. All other exceptions inherit from this.

    """
    pass


class InvalidPropertyError(FormationError):
    """
    Exception raised when user supplied properties are invalid.

    """
    pass
