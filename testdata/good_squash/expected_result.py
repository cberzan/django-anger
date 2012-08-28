# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        ### app_alpha app ###

        # Adding model 'Worm'
        db.create_table('app_alpha_worm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bottle', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('maker', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('good', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app_alpha', ['Worm'])

        # Adding M2M table for field books on 'Worm'
        db.create_table('app_alpha_worm_book', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('worm', models.ForeignKey(orm['app_alpha.worm'], null=False)),
            ('book', models.ForeignKey(orm['app_beta.book'], null=False))
        ))
        db.create_unique('app_alpha_worm_book', ['gcchecklist_id', 'book_id'])

        # Adding model 'Spoon'
        db.create_table('app_alpha_spoon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('worm', self.gf('django.db.models.fields.related.OneToOneField')(default=orm['app_alpha.Worm'], related_name='wormy', unique=True, to=orm['app_alpha.Worm'])),
            ('angle', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('app_alpha', ['Spoon'])

        # Adding model 'Champaigne'
        db.create_table('app_alpha_champaigne', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('blarg', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('foobar', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
        ))
        db.send_create_signal('app_alpha', ['Champaigne'])

        # Adding model 'Keyboard'
        db.create_table('app_alpha_keyboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('frog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='keyboards', to=orm['app_delta.Frog'])),
            ('bottle', self.gf('django.db.models.fields.related.ForeignKey')(related_name='keyboards', to=orm['app_delta.Bottle'])),
            ('tongue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='keyboards', to=orm['app_gamma.Tongue'])),
            ('champaigne', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_alpha.Champaigne'])),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('spoon', self.gf('django.db.models.fields.related.OneToOneField')(related_name='app_alpha', unique=True, to=orm['app_alpha.Spoon'])),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_beta.Book'])),
        ))
        db.send_create_signal('app_alpha', ['Keyboard'])


        ### app_beta app ###

        # Adding model 'Book'
        db.create_table('app_beta_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword_1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('keyword_2', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('toc', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('demo_omelet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_delta.Omelet'], null=True)),
        ))
        db.send_create_signal('app_beta', ['Book'])


        ### app_delta app ###

        # Adding model 'Frog'
        db.create_table('app_delta_frog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, null=True)),
            ('color', self.gf('django.db.models.fields.CharField')(default='green', max_length=50)),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('tongue_1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='frog_1', null=True, to=orm['app_gamma.Tongue'])),
            ('tongue_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='frog_2', to=orm['app_gamma.Tongue'])),
        ))
        db.send_create_signal('app_delta', ['Frog'])

        # Adding model 'Omelet'
        db.create_table('app_delta_omelet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('frog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_delta.Frog'], null=True)),
            ('ingredient_1', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('ingredient_2', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('ingredient_3', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('is_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app_delta', ['Omelet'])

        # Adding unique constraint on 'Omelet', fields ['frog', 'is_done']
        db.create_unique('app_delta_omelet', ['frog_id', 'is_done'])

        # Adding model 'Bottle'
        db.create_table('app_delta_bottle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('top', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('bottom', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('obtained', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('app_delta', ['Bottle'])


        ### app_gamma app ###

        # Adding model 'Thingy'
        db.create_table('app_gamma_thingy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=300)),
            ('mine', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('yours', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('app_gamma', ['Thingy'])

        # Adding model 'Shiny'
        db.create_table('app_gamma_shiny', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thingy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_gamma.Thingy'])),
            ('bender1', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('bender2', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('app_gamma', ['Shiny'])

        # Adding model 'Tongue'
        db.create_table('app_gamma_tongue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, null=True)),
            ('thingy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_gamma.Thingy'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('app_gamma', ['Tongue'])


    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")


    models = {
        'app_alpha.champaigne': {
            'Meta': {'object_name': 'Champaigne'},
            'blarg': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'foobar': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
        },
        'app_alpha.keyboard': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Keyboard'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_beta.Book']"}),
            'bottle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'keyboards'", 'to': "orm['app_delta.Bottle']"}),
            'champaigne': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_alpha.Champaigne']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'frog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'keyboards'", 'to': "orm['app_delta.Frog']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'spoon': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'app_alpha'", 'unique': 'True', 'to': "orm['app_alpha.Spoon']"}),
            'tongue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'keyboards'", 'to': "orm['app_gamma.Tongue']"}),
        },
        'app_alpha.spoon': {
            'Meta': {'object_name': 'Spoon'},
            'angle': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'worm': ('django.db.models.fields.related.OneToOneField', [], {'default': "orm['app_alpha.Worm']", 'related_name': "'wormy'", 'unique': 'True', 'to': "orm['app_alpha.Worm']"}),
        },
        'app_alpha.worm': {
            'Meta': {'object_name': 'Worm'},
            'bottle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'good': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maker': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'thingy': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
        },
        'app_beta.book': {
            'Meta': {'object_name': 'Book'},
            'demo_omelet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_delta.Omelet']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'keyword_2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'toc': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
        },
        'app_delta.bottle': {
            'Meta': {'object_name': 'Bottle'},
            'bottom': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obtained': ('django.db.models.fields.DateField', [], {}),
            'top': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
        },
        'app_delta.frog': {
            'Meta': {'object_name': 'Frog'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'green'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'tongue_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'frog_1'", 'null': 'True', 'to': "orm['app_gamma.Tongue']", 'blank': 'True'}),
            'tongue_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'frog_2'", 'to': "orm['app_gamma.Tongue']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'}),
        },
        'app_delta.omelet': {
            'Meta': {'unique_together': "(('frog_id', 'is_done'),)", 'object_name': 'Omelet'},
            'frog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_delta.Frog']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient_1': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ingredient_2': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ingredient_3': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
        },
        'app_gamma.shiny': {
            'Meta': {'object_name': 'Shiny'},
            'bender1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'bender2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thingy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_gamma.Thingy']"}),
        },
        'app_gamma.thingy': {
            'Meta': {'ordering': "['name']", 'object_name': 'Thingy'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mine': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'yours': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
        },
        'app_gamma.tongue': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Tongue'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thingy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_gamma.Thingy']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'}),
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '75', 'unique': 'True'}),
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
        },
    }

    complete_apps = [
        'app_alpha',
        'app_beta',
        'app_delta',
        'app_gamma',
    ]
