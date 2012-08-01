import ast

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


