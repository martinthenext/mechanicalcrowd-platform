# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table('task_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['xlsx.Table'])),
            ('sheet', self.gf('django.db.models.fields.TextField')()),
            ('columns', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('header_location', self.gf('django.db.models.fields.TextField')(default='A1:')),
            ('data_location', self.gf('django.db.models.fields.TextField')(default='A2:')),
            ('wrong_rows_definition', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('task_definition', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('deduplicate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allowed_operations', self.gf('django.db.models.fields.TextField')(default='edit, delete')),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('task', ['Task'])

        # Adding model 'Row'
        db.create_table('task_row', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['task.Task'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('values', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='G', max_length=2)),
        ))
        db.send_create_signal('task', ['Row'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table('task_task')

        # Deleting model 'Row'
        db.delete_table('task_row')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
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
            'Meta': {'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'task.row': {
            'Meta': {'object_name': 'Row'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'G'", 'max_length': '2'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': "orm['task.Task']"}),
            'values': ('django.db.models.fields.TextField', [], {})
        },
        'task.task': {
            'Meta': {'object_name': 'Task'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allowed_operations': ('django.db.models.fields.TextField', [], {'default': "'edit, delete'"}),
            'columns': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'data_location': ('django.db.models.fields.TextField', [], {'default': "'A2:'"}),
            'deduplicate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'header_location': ('django.db.models.fields.TextField', [], {'default': "'A1:'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sheet': ('django.db.models.fields.TextField', [], {}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['xlsx.Table']"}),
            'task_definition': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'wrong_rows_definition': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
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