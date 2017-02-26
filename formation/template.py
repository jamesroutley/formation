# -*- coding: utf-8 -*-

import collections
import contextlib
import json

import yaml

from .atomic_template import AtomicTemplate


class Template(object):

    def __init__(self):
        self._templates = []

    def merge(self, template):
        self._templates.append(template)

    def to_json(self, indent=4, sort_keys=True, separators=(',', ': ')):
        return json.dumps(
            self.template, indent=indent,
            sort_keys=sort_keys, separators=separators
        )

    def to_yaml(self, default_flow_style=False):
        return yaml.safe_dump(
            self.template, default_flow_style=default_flow_style
        )

    @property
    def _outputs(self):
        outputs = {}
        for template in self._templates:
            outputs.update(template._outputs)
        return outputs

    @property
    def _parameters(self):
        parameters = {}
        for template in self._templates:
            parameters.update(template._parameters)
        return parameters

    @property
    def _resources(self):
        resources = {}
        for template in self._templates:
            resources.update(template._resources)
        return resources

    @property
    def template(self):
        with unique_atom_names(self._templates):
            template = {
                "Parameters": self._parameters,
                "Resources": self._resources,
                "Outputs": self._outputs
            }
        return template


def flatten(templates):
    flattened_templates = []
    for template in templates:
        if isinstance(template, AtomicTemplate):
            flattened_templates.append(template)
        else:
            # TODO: I'd like templates to be private, but accessing it here
            # isn't great.
            flattened_templates.extend(flatten(template._templates))
    return flattened_templates


@contextlib.contextmanager
def unique_atom_names(templates):
    # TODO: look into optimising this.
    flattened_templates = flatten(templates)
    old_names = {}
    name_counter = collections.Counter()
    for template in flattened_templates:
        name_counter.update([template.title])
        name_count = name_counter[template.title]
        if name_count > 1:
            temp_name = "".join([template.title, str(name_count - 1)])
            old_names[temp_name] = template.title
            template.title = temp_name
    yield
    for template in flattened_templates:
        if template.title in old_names:
            template.title = old_names[template.title]
