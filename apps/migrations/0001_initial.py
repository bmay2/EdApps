# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Apps'
        db.create_table('apps_apps', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('platform', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')(max_length=10, null=True, blank=True)),
            ('downloads', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')(max_length=10, null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('artwork', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('crawl_binary', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('apps', ['Apps'])


    def backwards(self, orm):
        # Deleting model 'Apps'
        db.delete_table('apps_apps')


    models = {
        'apps.apps': {
            'Meta': {'object_name': 'Apps'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'artwork': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'crawl_binary': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'downloads': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['apps']