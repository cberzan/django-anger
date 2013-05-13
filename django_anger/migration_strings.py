#!/usr/bin/env python

"""
Parse a South migration file, and display all strings contained therein.

This is handy when you want to make a migration public, without revealing what
the models / fields of your app actually are. Mangle the model / field names,
then glance through the strings to make sure you haven't forgotten anything.
Note that this tool only looks through the frozen models and complete_apps. In
particular, it will not show strings contained in comments, forwards(),
backwards(), etc.

Usage:
    migration_strings my_migration.py
"""

from django_anger.migration_utils import parse_migration


def _deep_add(target, data):
    """
    Descends through the given data structure (which can be a combination of
    dicts, lists, tuples, and strings) and adds all encountered strings to
    the target set, in lower case.
    """
    if isinstance(data, dict):
        for key, value in data.iteritems():
            _deep_add(target, key)
            _deep_add(target, value)
    elif isinstance(data, list) or isinstance(data, tuple):
        for item in data:
            _deep_add(target, item)
    elif isinstance(data, str):
        target.add(data)
    else:
        raise TypeError("Cannot unpack value of type {}.".format(type(data)))


def migration_strings(f):
    """
    """
    models, complete_apps = parse_migration(f)
    strings = set(complete_apps)
    _deep_add(strings, models)
    return strings


def main():
    import sys
    if len(sys.argv) != 2:
        print __doc__
        sys.exit(1)

    for string in sorted(list(migration_strings(open(sys.argv[1])))):
        print string
