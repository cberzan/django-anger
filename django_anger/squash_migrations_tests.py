import nose
import os
import subprocess
import sys
import tempfile

from django_anger.squash_migrations import get_south_apps
from django_anger.squash_migrations import get_migration_filenames
from django_anger.squash_migrations import get_path_of_sole_initial_migration
from django_anger.squash_migrations import squash_migrations
from django_anger.squash_migrations import make_dummy_migration


def assert_equal_ignorespace_with_diff(got_str, expected_path):
    """
    Return True if got_str == open(expected_path).read(), modulo white space.
    If the two are not equal, raise a nose assertion failure, write got_str to
    a temp file, and print out the diff between that file and expected_path.
    """
    expected = open(expected_path).read()
    if (got_str.replace(' ', '').replace('\n', '') !=
        expected.replace(' ', '').replace('\n', '')):
        # Using assert_equals on these huge strings results in an unusable
        # error message. Run a diff instead.
        print >>sys.stderr, "Squashed migration does not match expected result."
        _, tmp_path = tempfile.mkstemp()
        open(tmp_path, 'w').write(got_str)
        print >>sys.stderr, "Wrote result to {}.".format(tmp_path)
        print >>sys.stderr, "Diff between got_str and expected (ignore whitespace):"
        subprocess.call(["diff", tmp_path, expected_path])
        nose.tools.assert_true(False, msg="Squashed migration does not match expected result.")


def get_south_apps_test():
    nose.tools.assert_equal(
        set(get_south_apps("testdata/good_squash/")),
        set(['app_alpha', 'app_beta', 'app_gamma', 'app_delta'])
    )


def get_migration_filenames_test():
    nose.tools.assert_equal(
        get_migration_filenames("testdata/good_squash/app_alpha/"),
        ['0001_initial.py']
    )
    nose.tools.assert_equal(
        set(get_migration_filenames("testdata/bad_squash/app_has_noninitial_migrations/")),
        set(['0001_initial.py', '0002_another.py'])
    )
    with nose.tools.assert_raises(OSError):
        get_migration_filenames("testdata/bad_squash/app_has_no_migrations/")


def get_path_of_sole_initial_migration_test():
    nose.tools.assert_equal(
        get_path_of_sole_initial_migration("testdata/good_squash/app_alpha/"),
        "testdata/good_squash/app_alpha/migrations/0001_initial.py"
    )
    with nose.tools.assert_raises(ValueError):
        get_path_of_sole_initial_migration("testdata/bad_squash/app_has_noninitial_migrations/")
    with nose.tools.assert_raises(ValueError):
        get_path_of_sole_initial_migration("testdata/bad_squash/app_has_no_initial_migration/")


def squash_migrations_test():
    project_dir = "testdata/good_squash/"
    apps = get_south_apps(project_dir)
    app_to_migration_path = {}
    for app in apps:
        app_dir = os.path.join(project_dir, app)
        app_to_migration_path[app] = \
            get_path_of_sole_initial_migration(app_dir)
    squashed_migration = squash_migrations(app_to_migration_path)
    got = squashed_migration.getvalue()
    expected_path = "testdata/good_squash/expected_result.py"
    assert_equal_ignorespace_with_diff(got, expected_path)
    # This is not really a good test, because the two files don't actually have
    # to be equal (modulo white space). For example, apps in forwards() and
    # models in models = {} can come any order.


def make_dummy_migration_test():
    project_dir = "testdata/good_squash/"
    app = 'app_gamma'
    app_dir = os.path.join(project_dir, app)
    migration_path = get_path_of_sole_initial_migration(app_dir)
    destination_app = app
    squashed_migration_name = "0001_everything"
    dummy_migration = make_dummy_migration(app, migration_path,
                                           destination_app,
                                           squashed_migration_name)
    got = dummy_migration.getvalue()
    expected_path = "testdata/good_squash/expected_new_initial.py"
    assert_equal_ignorespace_with_diff(got, expected_path)
    # This is not really a good test, because the two files don't actually have
    # to be equal (modulo white space). For example, apps in forwards() and
    # models in models = {} can come any order.
