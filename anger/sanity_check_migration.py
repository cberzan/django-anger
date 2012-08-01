#!/usr/bin/env python

"""
TODO
"""

from anger.utils import parse_migration


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
        # Check if this line starts a new model definition.
        for model in models.keys():
            # Fragile string-based matching.
            if "'{}':".format(model) in line:
                current_model = model
                fields_found = {}
        # Check if this line is a field definition.
        if current_model:
            for field in models[current_model].keys():
                # Fragile string-based matching.
                if "'{}':".format(field) in line:
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
