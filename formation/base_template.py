# -*- coding: utf-8 -*-

"""
formation.base_template implements the BaseTemplate class

"""

import abc
import json

import yaml


class BaseTemplate(object):
    """
    BaseTemplate implements methods to return JSON and YAML template strings.

    It is an abstact base class, so cannot be instantiated directly. Inheriting
    classes should add a variable (or property) ``self._template``, which
    should be assigned to the template dictionary.

    """

    __metaclass__ = abc.ABCMeta
    _template = None

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
