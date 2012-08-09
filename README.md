Tools and hacks for using Django "in anger".

http://english.stackexchange.com/questions/30939/is-used-in-anger-a-britishism-for-something


## Sanity-checking a South migration

From the directory containing `anger`:

```
python -m anger.sanity_check_migration my_migration.py
```

From Python:

```
from anger.sanity_check_migration import validate_migration_file
validate_migration_file(open('my_migration.py'))
```


## Squashing initial migrations into one

This is useful when you have circular dependencies. See ResettingMigrations.md.

Usage:

Suppose you git-cloned django-anger at `$ANGER`, your Django project is at
`$PROJECT`, and you have `app_alpha`, `app_beta`, and `app_gamma`, each with an
initial migration. To create a combined migration, put it in `app_alpha`, and
update the other initial migrations to depend on this combined migration, run:

```
cd $PROJECT
PYTHONPATH=$ANGER python -m anger.squash_migrations app_alpha
```

Again, read ResettingMigrations.md for the gory details.


## Displaying the strings contained in a South migration.

From the directory containing `anger`:

```
python -m anger.migration_strings my_migration.py
```

From Python:

```
from anger.migration_strings import migration_strings
migration_strings(open('my_migration.py'))
```


## Running the unit tests

From the directory containing `anger` and `testdata`:

```
nosetests --with-doctest anger
```
