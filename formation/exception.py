# -*- coding: utf-8 -*-

"""
formation.exception implements the exceptions raised by Formation.

"""


class FormationError(Exception):
    """
    Formation's base exception. All other exceptions inherit from this.

    This base exception can be caught in a try/except block to catch all custom
    errors thrown by Formation.

    e.g::

        from formation.exception import FormationError
        try:
            # Formation code that may error
        except FormationError:
            # Error handling code here

    """
    pass


class InvalidPropertyError(FormationError):
    """
    Exception raised when user supplied properties are invalid. This happens
    when an AtomicTemplate contains a required resource-specific parameter
    which is not supplied by the user. Formation cannot automatically
    parameterise required resource-specific parameters.

    """
    pass
