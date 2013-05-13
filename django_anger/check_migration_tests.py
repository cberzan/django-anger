import nose

from django_anger.check_migration import check_duplicate_fields
from django_anger.check_migration import check_duplicate_models
from django_anger.check_migration import check_gratuitous_frozen_models
from django_anger.check_migration import check_missing_related_models
from django_anger.check_migration import check_model_names
from django_anger.check_migration import ValidationError


def check_model_names_test():
    check_model_names(open("testdata/good_migration.py"))
    with nose.tools.assert_raises(ValidationError):
        check_model_names(open("testdata/bad_migration_bad_model_name_1.py"))
    with nose.tools.assert_raises(ValidationError):
        check_model_names(open("testdata/bad_migration_bad_model_name_2.py"))


def check_duplicate_models_test():
    check_duplicate_models(open("testdata/good_migration.py"))
    with nose.tools.assert_raises(ValidationError):
        check_duplicate_models(open("testdata/bad_migration_model_frozen_twice.py"))


def check_duplicate_fields_test():
    check_duplicate_fields(open("testdata/good_migration.py"))
    with nose.tools.assert_raises(ValidationError):
        check_duplicate_fields(open("testdata/bad_migration_field_frozen_twice.py"))


def check_missing_foreign_keys_test():
    check_missing_related_models(open("testdata/good_migration.py"))
    with nose.tools.assert_raises(ValidationError):
        check_missing_related_models(open("testdata/bad_migration_missing_foreign_key.py"))


def check_gratuitous_frozen_models_test():
    check_gratuitous_frozen_models(open("testdata/good_migration.py"))
    with nose.tools.assert_raises(ValidationError):
        check_gratuitous_frozen_models(open("testdata/bad_migration_gratuitous_frozen_model.py"))
