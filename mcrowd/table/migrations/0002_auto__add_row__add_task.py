# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Row'
        db.create_table('table_row', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['table.Task'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('values', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='G', max_length=2)),
        ))
        db.send_create_signal('table', ['Row'])

        # Adding model 'Task'
        db.create_table('table_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['table.Table'])),
            ('sheet', self.gf('django.db.models.fields.TextField')()),
            ('columns', self.gf('django.db.models.fields.TextField')()),
            ('header_location', self.gf('django.db.models.fields.TextField')()),
            ('data_location', self.gf('django.db.models.fields.TextField')()),
            ('wrong_rows_definition', self.gf('django.db.models.fields.TextField')()),
            ('task_definition', self.gf('django.db.models.fields.TextField')()),
            ('deduplicate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('table', ['Task'])


    def backwards(self, orm):
        # Deleting model 'Row'
        db.delete_table('table_row')

        # Deleting model 'Task'
        db.delete_table('table_task')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'table.row': {
            'Meta': {'object_name': 'Row'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'G'", 'max_length': '2'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['table.Task']"}),
            'values': ('django.db.models.fields.TextField', [], {})
        },
        'table.table': {
            'Meta': {'object_name': 'Table'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'table': ('django.db.models.fields.BinaryField', [], {})
        },
        'table.task': {
            'Meta': {'object_name': 'Task'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'columns': ('django.db.models.fields.TextField', [], {}),
            'data_location': ('django.db.models.fields.TextField', [], {}),
            'deduplicate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'header_location': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sheet': ('django.db.models.fields.TextField', [], {}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['table.Table']"}),
            'task_definition': ('django.db.models.fields.TextField', [], {}),
            'wrong_rows_definition': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['table']