# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
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

    def backwards(self, orm):
        # Deleting model 'Worm'
        db.delete_table('app_alpha_worm')

        # Removing M2M table for field books on 'Worm'
        db.delete_table('app_alpha_worm_book')

        # Deleting model 'Spoon'
        db.delete_table('app_alpha_spoon')

        # Deleting model 'Champaigne'
        db.delete_table('app_alpha_champaigne')

        # Deleting model 'Keyboard'
        db.delete_table('app_alpha_keyboard')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'app_gamma.thingy': {
            'Meta': {'ordering': "['name']", 'object_name': 'Thingy'},
            'yours': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mine': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
        },
        'app_gamma.tongue': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Tongue'},
            'thingy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_gamma.Thingy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        'app_alpha.spoon': {
            'Meta': {'object_name': 'Spoon'},
            'worm': ('django.db.models.fields.related.OneToOneField', [], {'default': "orm['app_alpha.Worm']", 'related_name': "'wormy'", 'unique': 'True', 'to': "orm['app_alpha.Worm']"}),
            'angle': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        },
        'app_alpha.champaigne': {
            'Meta': {'object_name': 'Champaigne'},
            'blarg': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'foobar': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'app_alpha.worm': {
            'Meta': {'object_name': 'Worm'},
            'thingy': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'bottle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'good': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maker': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
        },
        'app_alpha.keyboard': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Keyboard'},
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'bottle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'keyboards'", 'to': "orm['app_delta.Bottle']"}),
            'frog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'keyboards'", 'to': "orm['app_delta.Frog']"}),
            'tongue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'keyboards'", 'to': "orm['app_gamma.Tongue']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'champaigne': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_alpha.Champaigne']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'spoon': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'app_alpha'", 'unique': 'True', 'to': "orm['app_alpha.Spoon']"}),
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_beta.Book']"}),
        },
        'app_delta.bottle': {
            'Meta': {'object_name': 'Bottle'},
            'obtained': ('django.db.models.fields.DateField', [], {}),
            'top': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'bottom': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
        },
        'app_delta.frog': {
            'Meta': {'object_name': 'Frog'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'green'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'tongue_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'frog_2'", 'to': "orm['app_gamma.Tongue']"}),
            'tongue_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'frog_1'", 'null': 'True', 'to': "orm['app_gamma.Tongue']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        'app_beta.book': {
            'Meta': {'object_name': 'Book'},
            'toc': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'keyword_2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'demo_omelet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_delta.Omelet']", 'null': 'True'}),
        },
        'app_delta.omelet': {
            'Meta': {'unique_together': "(('frog_id', 'is_done'),)", 'object_name': 'Omelet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ingredient_1': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ingredient_2': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ingredient_3': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'frog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_delta.Frog']", 'null': 'True'}),
        },
    }

    complete_apps = ['app_alpha']
