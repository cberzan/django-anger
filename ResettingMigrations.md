# Resetting South migrations

This document explains how to reset the South migrations in a large Django
project, where models in different apps reference each other circularly. If
you're uncomfortable with South and editing migrations by hand makes you
queasy, this is probably not for you. Head over to the [South docs][south-docs]
and read their tutorial instead.



## Motivation

You have a project with lots of migrations. These migrations are executed every
time you run your tests, and that takes too much time. You want to forget the
entire migration history, and start from scratch with a single initial
migration in each app.



## Step 1: Reset migrations in each app

The first step is to reset the migration history in each app, as described in
[this answer on Stack Overflow][so-answer]. Basically, delete all migrations:

```sh
cd $PROJECT
rm */migrations/*
```

and then create a new initial migration in each app:

```sh
for migrations_dir in $(ls -d */migrations); do
    app=$(dirname $migrations_dir)
    ./manage.py convert_to_south $app
done
```



## Step 2: Squash initial migrations into one

You can try applying your new initial migrations to an empty DB. If this works,
you're done! Congratulations.

But often you will run into issues with circular dependencies between apps.
For example, `app1.Grunt` has a ForeignKey to `app2.Hurr`, and `app2.Grumble`
has a ForeignKey to `app1.Hrm`. No matter in what order you run the initial
migrations, they will fail, because some model doesn't exist yet.

The solution is to squash the initial migrations for each app into a SINGLE
initial migration for ALL apps. **django-anger** has a script for this:

```sh
cd $PROJECT
# this will create the squashed migration in app1/migrations/0001_everything.py
squash_migrations app1
```

This generates a new migration `app1/migrations/0001_everything.py`, which
creates the tables and relationships for ALL apps. It also modifies the initial
migration in each app to be a no-op migration that depends on
`0001_everything`. By having the meat of all initial migrations squashed into a
single migration, you avoid all circular-dependency issues.



## Step 3: Deploy this to production

This step is necessarily vague, because it depends on how your Django project
is deployed. In broad strokes, you have to do the following:

On a development machine, dump the new `MigrationHistory` table. This is the
rewritten migration history that we have obtained by resetting migrations.

```sh
./manage.py dumpdata south --natural >dump.json
```

On the production machine, drop the old `MigrationHistory` table, and load the
new one from the dump you just created:

```sh
./manage.py reset south
./manage.sh loaddata dump.json
```

Of course, you should test this process on a staging machine before trying it
in production.

That's it! Keep reading if you want to know more details about how
`squash_migrations` works.



## Background: The structure of a South migration

Let's recap this to make sure we're on the same page.

```python
# File: app1/migrations/0010_add_foo_model.py

# various imports

class Migration(SchemaMigration):

    def forwards(self, orm):
        # This method APPLIES the changes described in this migration.
        # It brings the app's schema from the state frozen in 0009 (the
        # previous migration) to the state frozen in 0010 (this migration).

    def backwards(self, orm):
        # This method UNDOES the changes described in this migration.
        # It brings the app's schema from the state frozen in 0010 (this
        # migration) to the state frozen in 0009 (the previous migration).

    models = {
        # This dicts holds a representation of all the relevant models AFTER
        # this migration's forwards() method was run. For each model, we have
        # the field names, types, parameters, and Meta attributes saved here.
    }

    # If an app is in this list, then ALL its models are frozen above.
    # If an app is NOT in this list, SOME of its models might still be
    # frozen above, e.g. if they are referenced by other frozen models.
    complete_apps = ['app1']
```



## Background: The squashed migration

The squashed migration is exactly what it sounds like --
a combination of the initial migrations from ALL your apps.

```python
# File: app1/migrations/0001_everything.py

# various imports

class Migration(SchemaMigration):

    def forwards(self, orm):
        # The concatenated forwards() methods from
        # the initial migrations of ALL your apps.

    def backwards(self, orm):
        # No undo. Just raise an exception.

    models = {
        # The union of the models frozen in the
        # initial migrations of ALL your apps.
    }

    complete_apps = [
        # ALL your apps.
    ]
```



## Background: Deferred magic in South

Alert readers will wonder why there are no order / dependency issues in the
squashed migration. Consider this `forwards()` method:

```python
def forwards(self, orm):

    # Adding model 'Hrm'
    db.create_table('app1_hrm', (
        ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ('grumble', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['app1.grumble'], null=True, blank=True)),
    ))
    db.send_create_signal('app1', ['Hrm'])

    # Adding model 'Grumble'
    db.create_table('app1_grumble', (
        ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
    ))
    db.send_create_signal('app1', ['Grumble'])
```

Notice how `Hrm` has a ForeignKey to `Grumble`, but `Hrm` gets created first.
So `Grumble` is referenced before it gets created. Does this work? Yes! But
why? Because South is clever. It defers the ForeignKeys and other relational
constraints, and adds them only AFTER it finishes creating ALL tables.



[so-answer]: http://stackoverflow.com/a/4656070
[south-docs]: http://south.readthedocs.org/en/latest/index.html
