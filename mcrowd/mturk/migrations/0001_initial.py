# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Turker'
        db.create_table('mturk_turker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ident', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=40)),
        ))
        db.send_create_signal('mturk', ['Turker'])

        # Adding model 'Hit'
        db.create_table('mturk_hit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hits', to=orm['task.Task'])),
            ('ident', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=40)),
            ('values', self.gf('django.db.models.fields.TextField')()),
            ('upper_task', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('lower_task', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('functions', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('reward', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
            ('max_assignments', self.gf('django.db.models.fields.IntegerField')()),
            ('disabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mturk', ['Hit'])

        # Adding model 'Assignment'
        db.create_table('mturk_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ident', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=40)),
            ('hit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignments', to=orm['mturk.Hit'])),
            ('turker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignments', to=orm['mturk.Turker'])),
            ('token', self.gf('django.db.models.fields.TextField')()),
            ('done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mturk', ['Assignment'])


    def backwards(self, orm):
        # Deleting model 'Turker'
        db.delete_table('mturk_turker')

        # Deleting model 'Hit'
        db.delete_table('mturk_hit')

        # Deleting model 'Assignment'
        db.delete_table('mturk_assignment')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mturk.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['mturk.Hit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '40'}),
            'token': ('django.db.models.fields.TextField', [], {}),
            'turker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['mturk.Turker']"})
        },
        'mturk.hit': {
            'Meta': {'object_name': 'Hit'},
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'functions': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '40'}),
            'lower_task': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'max_assignments': ('django.db.models.fields.IntegerField', [], {}),
            'reward': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hits'", 'to': "orm['task.Task']"}),
            'upper_task': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'values': ('django.db.models.fields.TextField', [], {})
        },
        'mturk.turker': {
            'Meta': {'object_name': 'Turker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '40'})
        },
        'task.task': {
            'Meta': {'object_name': 'Task'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'columns': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'deduplicate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delete_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['xlsx.Table']"}),
            'task_definition': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'wrong_rows_definition': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'xlsx.table': {
            'Meta': {'object_name': 'Table'},
            'col_ids': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'col_names': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'data_location': ('django.db.models.fields.CharField', [], {'default': "'A2:'", 'max_length': '20'}),
            'header_location': ('django.db.models.fields.CharField', [], {'default': "'A1:'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'worksheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['xlsx.Worksheet']"})
        },
        'xlsx.workbook': {
            'Meta': {'object_name': 'Workbook', 'unique_together': "(('owner', 'filename'),)"},
            'data': ('django.db.models.fields.BinaryField', [], {}),
            'filename': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'xlsx.worksheet': {
            'Meta': {'object_name': 'Worksheet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'workbook': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sheets'", 'to': "orm['xlsx.Workbook']"})
        }
    }

    complete_apps = ['mturk']