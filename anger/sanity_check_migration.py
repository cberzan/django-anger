#!/usr/bin/env python

"""
TODO
"""

import re

from anger.utils import model_start_re
from anger.utils import skip_lines_until_frozen_models


class ValidationError(Exception):
    pass


validators = []


def register_validator(func):
    validators.append(func)
    return func


@register_validator
def check_missing_foreign_keys(f):
    """
    Verify that for all ForeignKeys referenced in model fields, the destination
    model is also frozen.
    """
    # Collect all models referenced as ForeignKeys.
    # Example:
    # 

    
@register_validator
def check_duplicate_models(f):
    """
    Verify that no model is frozen twice.
    """


@register_validator
def check_duplicate_fields(f):
    """
    Verify that no model has the same field frozen twice.
    """


@register_validator
def check_model_names(f):
    """
    Verify that the frozen model name is lowercase and matches the capitalized
    model name in Meta.
    """
    # Example:
    #     'app_zeta.model15': {
    #         'Meta': {'ordering': "['qpwepzldn']", 'object_name': 'Model15'},
    meta_re = re.compile("^ *'Meta': {.*'object_name': '([a-zA-Z0-9_]+)'.*},$")
    skip_lines_until_frozen_models(f)
    while True:
        try:
            line = f.next()
        except StopIteration:
            break
        line1_match = model_start_re.match(line)
        if not line1_match:
            continue
        line2_match = meta_re.match(f.next())
        if not line2_match:
            raise ValidationError("Could not grok the line after "
                                  "this line: '{}'.".format(line))
        lowercase_model_name = line1_match.group(2)
        capitalized_model_name = line2_match.group(1)
        if lowercase_model_name.lower() != lowercase_model_name:
            raise ValidationError("Expected lower-case app.model_name, but "
                                  "found '{}'.".format(lowercase_model_name))
        if capitalized_model_name.lower() != lowercase_model_name:
            raise ValidationError("Meta object_name '{}' does not match "
                                  "expected model name '{}'.".format(
                                      capitalized_model_name,
                                      lowercase_model_name))


@register_validator
def check_gratuitous_frozen_models(f):
    """
    Verify that a model is frozen only if it is in a complete_apps app, or if it
    is referenced as a ForeignKey.
    """


def validate_migration_file(f):
    """
    Run all the validators in sequence, propagating any exceptions they might
    raise.
    """
    for validator in validators:
        validator(f)
        f.seek(0)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(1)

    for migration in sys.argv[1:]:
        print "Validating {}...".format(migration)
        try:
            f = open(migration)
            validate_migration_file(f)
            print " -> OK."
        except Exception as err:
            print " -> failed: {}".format(err)
            print "\nFull traceback:\n"
            import traceback
            traceback.print_exc()
            sys.exit(1)

    print "\nAll is well in the world."
