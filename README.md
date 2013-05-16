Tools and hacks for using Django [_in
anger_](http://english.stackexchange.com/q/30939).


## Installing

```sh
pip install django-anger
```

## Sanity-checking South migrations

This is useful to make sure you didn't break anything, in case you had to do
some manual surgery on migration files. You can pass one or multiple files.

```sh
check_migration migration_1.py [migration_2.py ...]
```


## Squashing initial migrations into one

This is useful when you want to [reset your migration
history](ResettingMigrations.md), but you have circular
dependencies between your apps.

```sh
# All apps in your Django project must have only an initial migration.
# Say you want to save the squashed migration in app_alpha.
squash_migrations app_alpha
```

Please read [ResettingMigrations.md](ResettingMigrations.md) for details.


## Displaying the strings contained in a South migration.

This is useful to make sure you haven't left any proprietary strings in a
migration you want to publish.

```sh
migration_strings my_migration.py
```


## Running the unit tests

From the directory containing `anger` and `testdata`:

```sh
nosetests --with-doctest django_anger
```
