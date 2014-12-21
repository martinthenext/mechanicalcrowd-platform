# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'RowDiff.row'
        db.delete_column('task_rowdiff', 'row_id')

        # Adding field 'RowDiff.task'
        db.add_column('task_rowdiff', 'task',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task.Task'], related_name='diff', default=0),
                      keep_default=False)

        # Adding field 'RowDiff.number'
        db.add_column('task_rowdiff', 'number',
                      self.gf('django.db.models.fields.IntegerField')(db_index=True, default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'RowDiff.row'
        db.add_column('task_rowdiff', 'row',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task.Row'], related_name='diff', default=0),
                      keep_default=False)

        # Deleting field 'RowDiff.task'
        db.delete_column('task_rowdiff', 'task_id')

        # Deleting field 'RowDiff.number'
        db.delete_column('task_rowdiff', 'number')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'task.row': {
            'Meta': {'object_name': 'Row'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'G'"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['task.Task']", 'related_name': "'rows'"}),
            'values': ('django.db.models.fields.TextField', [], {})
        },
        'task.rowdiff': {
            'Meta': {'object_name': 'RowDiff'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['task.Task']", 'related_name': "'diff'"}),
            'values': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'task.task': {
            'Meta': {'object_name': 'Task'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'columns': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'deduplicate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delete_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['xlsx.Table']", 'related_name': "'tasks'"}),
            'task_definition': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'wrong_rows_definition': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
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
            'workbook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['xlsx.Workbook']", 'related_name': "'sheets'"})
        }
    }

    complete_apps = ['task']