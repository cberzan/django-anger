Tools and hacks for using Django "in anger".

http://english.stackexchange.com/questions/30939/is-used-in-anger-a-britishism-for-something


## Sanity-checking a South migration

This is useful to make sure you didn't break anything, in case you had to do
some manual surgery on migration files.

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

This is useful when you want to [reset your migration
history](ResettingMigrations.md), but you have circular
dependencies between your apps.

Usage:

Suppose you git-cloned django-anger at `$ANGER`, your Django project is at
`$PROJECT`, and you have `app_alpha`, `app_beta`, and `app_gamma`, each with an
initial migration. To create a combined migration, put it in `app_alpha`, and
update the other initial migrations to depend on this combined migration, run:

```
cd $PROJECT
PYTHONPATH=$ANGER python -m anger.squash_migrations app_alpha
```

Please read [ResettingMigrations.md](ResettingMigrations.md) for details.


## Displaying the strings contained in a South migration.

This is useful to make sure you haven't left any proprietary strings in a
migration you want to publish.

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
