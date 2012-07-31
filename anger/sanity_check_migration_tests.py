import nose

from anger.sanity_check_migration import check_model_names
from anger.sanity_check_migration import ValidationError


def check_model_names_test():
    check_model_names(open("testdata/good_migration.py"))
    with nose.tools.assert_raises(ValidationError):
        check_model_names(open("testdata/bad_migration_bad_model_name_1.py"))
    with nose.tools.assert_raises(ValidationError):
        check_model_names(open("testdata/bad_migration_bad_model_name_2.py"))
