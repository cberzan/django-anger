#!/usr/bin/env python

"""
These are very UGLY and FRAGILE hacks to tease out the strings out of a mangled
migration, and visually inspect them to make sure we're not leaking any secrets.
"""

import re

from anger.utils import model_start_re
from anger.utils import skip_lines_until_frozen_models


def app_names(f):
    """
    Return set of all app names mentioned in the migration.
    """
    # Example:
    # ...
    # models = {
    #     'auth.group': {
    #         'Meta': {'object_name': 'Group'},
    #          ...
    #     },
    #     ...
    # }
    # ...
    skip_lines_until_frozen_models(f)
    app_names = set()
    for line in f:
        match = model_start_re.match(line)
        if match:
            app_names.add(match.group(1))
    return app_names


def model_names(f):
    """
    Return set of all model names mentioned in the migration.
    """
    # Example:
    # ...
    # models = {
    #     'auth.group': {
    #         'Meta': {'object_name': 'Group'},
    #          ...
    #     },
    #     ...
    # }
    # ...
    skip_lines_until_frozen_models(f)
    model_names = set()
    for line in f:
        match = model_start_re.match(line)
        if match:
            model_names.add(match.group(2))
    return model_names


def field_names(f):
    """
    Return set of all field names mentioned in the migration.
    """
    # Example:
    # ...
    # models = {
    #     'auth.group': {
    #         'Meta': {'object_name': 'Group'},
    #         'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
    #          ...
    #     },
    #     ...
    # }
    # ...
    skip_lines_until_frozen_models(f)
    model_field_re = re.compile("^ *\'([a-z0-9_]+)': \(.*\),$")
    field_names = set()
    for line in f:
        match = model_field_re.match(line)
        if match:
            field_names.add(match.group(1))
    return field_names


def related_names(f):
    """
    Return set of all related_name = '...' entries mentioned in the migration.
    """
    # Example:
    #         'field047': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'asdf'", 'null': 'True', 'to': "orm['app_delta.Model11']"}),
    skip_lines_until_frozen_models(f)
    related_name_re = re.compile("'related_name': \"'([a-zA-Z0-9_]+)'\"")
    related_names = set()
    for line in f:
        match = related_name_re.search(line)
        if match:
            related_names.add(match.group(1))
    return related_names


def defaults(f):
    """
    Return set of all default = '...' entries mentioned in the migration.
    """
    # Example:
    #         'field068': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '7', 'decimal_places': '2'}),
    skip_lines_until_frozen_models(f)
    default_re = re.compile("'default': \"'([^']+)'\"")  # breaks on escaped \'
    defaults = set()
    for line in f:
        match = default_re.search(line)
        if match:
            defaults.add(match.group(1))
    return defaults


def orderings(f):
    """
    Yields (line_no, col_no, ordering_val) for all ordering = '...' entries
    mentioned in the migration.
    """
    # Example:
    #         'Meta': {'ordering': "['qpwepzldn']", 'object_name': 'Model15'},
    skip_lines_until_frozen_models(f)
    ordering_re = re.compile("'ordering': \"\[([^\[\]]+)\]\"")  # breaks on escaped \[, \]
    orderings = set()
    for line in f:
        match = ordering_re.search(line)
        if match:
            orderings.add(match.group(1))
    return orderings
