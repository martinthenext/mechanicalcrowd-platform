# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Assignment.approved'
        db.alter_column('mturk_assignment', 'approved', self.gf('django.db.models.fields.BooleanField')())

    def backwards(self, orm):

        # Changing field 'Assignment.approved'
        db.alter_column('mturk_assignment', 'approved', self.gf('django.db.models.fields.NullBooleanField')(null=True))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mturk.assignment': {
            'Meta': {'unique_together': "(('ident', 'turker', 'token'),)", 'object_name': 'Assignment'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['mturk.Hit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True', 'db_index': 'True'}),
            'token': ('django.db.models.fields.TextField', [], {}),
            'turker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['mturk.Turker']"})
        },
        'mturk.hit': {
            'Meta': {'object_name': 'Hit'},
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'functions': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True', 'db_index': 'True'}),
            'lower_task': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'max_assignments': ('django.db.models.fields.IntegerField', [], {}),
            'reward': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '3'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hits'", 'to': "orm['task.Task']"}),
            'upper_task': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'values': ('django.db.models.fields.TextField', [], {})
        },
        'mturk.turker': {
            'Meta': {'object_name': 'Turker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True', 'db_index': 'True'})
        },
        'task.task': {
            'Meta': {'object_name': 'Task'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'columns': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'deduplicate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delete_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'hits_per_user': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['xlsx.Table']"}),
            'task_definition': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'wrong_rows_definition': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"})
        },
        'xlsx.table': {
            'Meta': {'object_name': 'Table'},
            'col_ids': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'col_names': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'data_location': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'A2:'"}),
            'header_location': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'A1:'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'worksheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['xlsx.Worksheet']"})
        },
        'xlsx.workbook': {
            'Meta': {'unique_together': "(('owner', 'filename'),)", 'object_name': 'Workbook'},
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