import ast
import re


def forwards_contents(f):
    """
    Return a string containing everything in the forwards() method of a
    migration.

    This string may not be safe to evaluate.
    """
    forwards_found = False
    forwards_lines = []
    for line in f:
        if 'def backwards(self, orm):' in line:
            break
        if forwards_found:
            forwards_lines.append(line)
        elif 'def forwards(self, orm):' in line:
            forwards_found = True
    return ''.join(forwards_lines)


def parse_migration(f):
    """
    Parse migration file and return (frozen_models, complete_apps).

    The returned objects are full-fledged Python data structures, as if we
    actually imported the migration file. But because we use ast.literal_eval(),
    this is safe to run on untrusted code.
    """
    # Collect lines defining models and complete_apps.
    # Example:
    # models = {
    #     ...
    # }
    # complete_apps = ['app_beta', 'app_gamma']
    model_lines = []
    complete_apps_lines = []
    models_found = False
    complete_apps_found = False
    for line in f:
        if not models_found and 'models =' in line:
            models_found = True
        if not complete_apps_found and 'complete_apps' in line:
            complete_apps_found = True
        if models_found and not complete_apps_found:
            model_lines.append(line)
        elif complete_apps_found:
            complete_apps_lines.append(line)
    if not models_found or not complete_apps_found:
        raise ValueError('Could not parse migration.')

    # Parse models.
    model_str = "".join(model_lines).strip()
    assert model_str.startswith('models =')
    model_str = model_str[len('models ='):]
    models = ast.literal_eval(model_str.strip())

    # Parse complete_apps.
    complete_apps_str = "".join(complete_apps_lines).strip()
    assert complete_apps_str.startswith('complete_apps =')
    complete_apps_str = complete_apps_str[len('complete_apps ='):]
    complete_apps = ast.literal_eval(complete_apps_str.strip())

    return models, complete_apps


def is_related(field):
    """
    Return True if the given field definition is a ForeignKey, OneToOneField, or
    ManyToManyField.

    >>> is_related(('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}))
    False
    >>> is_related(('django.db.models.fields.related.ForeignKey', [], {'related_name': "'asdfadfa'", 'to': "orm['app_zeta.Model15']"}))
    True
    >>> is_related(('django.db.models.fields.related.OneToOneField', [], {'to': "orm['app_delta.Model09']", 'unique': 'True', 'null': 'True'}))
    True
    >>> is_related(('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app_delta.Model13']", 'symmetrical': 'False'}))
    True
    """
    return field[0] in (
        'django.db.models.fields.related.ForeignKey',
        'django.db.models.fields.related.OneToOneField',
        'django.db.models.fields.related.ManyToManyField',
    )


def related_target(field):
    """
    Return target model of ForeignKey, OneToOneField, or ManyToManyField, as an
    "app.ModelName" string.

    >>> related_target(('django.db.models.fields.related.ForeignKey', [], {'related_name': "'asdfadfa'", 'to': "orm['app_zeta.Model15']"}))
    'app_zeta.Model15'
    >>> related_target(('django.db.models.fields.related.OneToOneField', [], {'to': "orm['app_delta.Model09']", 'unique': 'True', 'null': 'True'}))
    'app_delta.Model09'
    >>> related_target(('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app_delta.Model13']", 'symmetrical': 'False'}))
    'app_delta.Model13'
    """
    to_re = re.compile("^orm\['([^']+)'\]$")
    return to_re.match(field[2]['to']).group(1)

