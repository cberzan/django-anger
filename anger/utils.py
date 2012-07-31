import re

# Example:
#     'auth.group': {
#      (  ) (   )
model_start_re = re.compile("^ *\'([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)': {$")


def skip_lines_until_frozen_models(f):
    """
    Eat lines until start of frozen models.
    """
    for line in f:
        if 'models = {' in line:
            break
    else:
        raise RuntimeError("Could not find start of frozen models.")
