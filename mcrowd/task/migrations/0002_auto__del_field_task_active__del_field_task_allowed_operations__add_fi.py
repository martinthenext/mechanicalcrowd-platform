# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Task.active'
        db.delete_column('task_task', 'active')

        # Deleting field 'Task.allowed_operations'
        db.delete_column('task_task', 'allowed_operations')

        # Adding field 'Task.edit_allowed'
        db.add_column('task_task', 'edit_allowed',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Task.delete_allowed'
        db.add_column('task_task', 'delete_allowed',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Task.active'
        db.add_column('task_task', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Task.allowed_operations'
        db.add_column('task_task', 'allowed_operations',
                      self.gf('django.db.models.fields.TextField')(default='edit, delete'),
                      keep_default=False)

        # Deleting field 'Task.edit_allowed'
        db.delete_column('task_task', 'edit_allowed')

        # Deleting field 'Task.delete_allowed'
        db.delete_column('task_task', 'delete_allowed')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
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
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': "orm['task.Task']"}),
            'values': ('django.db.models.fields.TextField', [], {})
        },
        'task.task': {
            'Meta': {'object_name': 'Task'},
            'columns': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'data_location': ('django.db.models.fields.TextField', [], {'default': "'A2:'"}),
            'deduplicate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delete_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'header_location': ('django.db.models.fields.TextField', [], {'default': "'A1:'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sheet': ('django.db.models.fields.TextField', [], {}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['xlsx.Table']"}),
            'task_definition': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'wrong_rows_definition': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"})
        },
        'xlsx.table': {
            'Meta': {'object_name': 'Table'},
            'filename': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sheets': ('django.db.models.fields.TextField', [], {}),
            'table': ('django.db.models.fields.BinaryField', [], {})
        }
    }

    complete_apps = ['task']