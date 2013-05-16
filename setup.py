import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup

from django_anger import __version__


long_description = \
"""
Please see the docs at https://github.com/cberzan/django-anger.
"""

setup(
    name = "django-anger",
    version = __version__,
    packages = ["django_anger"],
    py_modules = ["distribute_setup"],

    # metadata for upload to PyPI
    author = "Constantin Berzan",
    author_email = "cberzan@gmail.com",
    description = "tools and hacks for using Django _in anger_",
    long_description = long_description,
    license = "MIT",
    keywords = "django south migration migrations",
    url = "https://github.com/cberzan/django-anger",
    # download_url =

    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ],

    entry_points = {
        'console_scripts': [
            'check_migration = django_anger.check_migration:main',
            'squash_migrations = django_anger.squash_migrations:main',
            'migration_strings = django_anger.migration_strings:main',
        ],
    },
)
