#!/usr/bin/env python

"""
Parse a South migration file, and do some basic sanity checking on it.

Usage:
    check_migration my_migration.py
"""

from django_anger.migration_utils import is_related
from django_anger.migration_utils import parse_migration
from django_anger.migration_utils import related_target


class ValidationError(Exception):
    pass


validators = []


def register_validator(func):
    validators.append(func)
    return func


@register_validator
def check_missing_related_models(f):
    """
    Verify that for all related models, the target model is also frozen.
    """
    models, complete_apps = parse_migration(f)
    for model, fields in models.iteritems():
        for field_name, field_def in fields.iteritems():
            if field_name == 'Meta':
                continue
            if not is_related(field_def):
                continue
            target = related_target(field_def).lower()
            if target not in models:
                raise ValidationError(
                    "Field '{}' has ForeignKey to model '{}', which is "
                    "not frozen.".format(field_name, target))


@register_validator
def check_duplicate_models(f):
    """
    Verify that no model is frozen twice.
    """
    # parse_migration() gives us a dict, which cannot have duplicate keys.
    # So we have to get messy and look at the raw file.
    models, complete_apps = parse_migration(f)
    found = {}
    f.seek(0)
    for line in f:
        for model in models.keys():
            # Fragile string-based matching.
            if "'{}':".format(model) in line:
                if model in found:
                    raise ValidationError(
                            "Model '{}' frozen twice.".format(model))
                found[model] = True


@register_validator
def check_duplicate_fields(f):
    """
    Verify that no model has the same field frozen twice.
    """
    # parse_migration() gives us dicts, which cannot have duplicate keys.
    # So we have to get messy and look at the raw file.
    models, complete_apps = parse_migration(f)
    current_model = None
    fields_found = {}
    f.seek(0)
    for line in f:
        line = line.strip()
        # Check if this line starts a new model definition.
        for model in models.keys():
            # Fragile string-based matching.
            if line.startswith("'{}': {{".format(model)):
                current_model = model
                fields_found = {}
        # Check if this line is a field definition.
        if current_model:
            for field in models[current_model].keys():
                # Fragile string-based matching.
                if line.startswith("'{}': (".format(field)):
                    if field in fields_found:
                        raise ValidationError(
                            "Field '{}' of model '{}' frozen twice.".format(
                                field, current_model))
                    fields_found[field] = True


@register_validator
def check_model_names(f):
    """
    Verify that the frozen model name is lowercase and matches the capitalized
    model name in Meta.
    """
    models, complete_apps = parse_migration(f)
    for model, fields in models.iteritems():
        app_name, lowercase_model_name = model.split('.')
        capitalized_model_name = fields['Meta']['object_name']
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
    is referenced by a ForeignKey.
    """
    models, complete_apps = parse_migration(f)
    related_targets = set()
    for model, fields in models.iteritems():
        for field_name, field_def in fields.iteritems():
            if field_name == 'Meta':
                continue
            if is_related(field_def):
                related_targets.add(related_target(field_def).lower())
    for model in models:
        app, model_name = model.split('.')
        if app not in complete_apps and model not in related_targets:
            raise ValidationError(
                    "Model '{}' frozen but not used.".format(model))


def validate_migration_file(f):
    """
    Run all the validators in sequence, propagating any exceptions they might
    raise.
    """
    for validator in validators:
        validator(f)
        f.seek(0)


def main():
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
