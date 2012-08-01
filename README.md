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

## Running the unit tests

From the directory containing `anger` and `testdata`:

```
nosetests --with-doctest anger
```
