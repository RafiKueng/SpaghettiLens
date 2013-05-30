# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LensData'
        db.create_table('ModellerApp_lensdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('datasource', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('datasource_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('img_data', self.gf('django.db.models.fields.TextField')()),
            ('add_data', self.gf('django.db.models.fields.TextField')()),
            ('n_res', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('created_by_str', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_accessed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('ModellerApp', ['LensData'])

        # Adding model 'Collection'
        db.create_table('ModellerApp_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('created_by_str', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('ModellerApp', ['Collection'])

        # Adding M2M table for field lenses on 'Collection'
        db.create_table('ModellerApp_collection_lenses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collection', models.ForeignKey(orm['ModellerApp.collection'], null=False)),
            ('lensdata', models.ForeignKey(orm['ModellerApp.lensdata'], null=False))
        ))
        db.create_unique('ModellerApp_collection_lenses', ['collection_id', 'lensdata_id'])

        # Adding model 'BasicLensData'
        db.create_table('ModellerApp_basiclensdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('catalog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ModellerApp.Catalog'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('catalog_img_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('n_res', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('requested_last', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('z_lens', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('z_source', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('img_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('channel1_imgurl', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('channel1_type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('channel1_data', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('channel2_imgurl', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('channel2_type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('channel2_data', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('channel3_imgurl', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('channel3_data', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('channel3_type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('channel4_imgurl', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('channel4_data', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('channel4_type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('channel5_imgurl', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('channel5_data', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('channel5_type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
        ))
        db.send_create_signal('ModellerApp', ['BasicLensData'])

        # Adding model 'Catalog'
        db.create_table('ModellerApp_catalog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('ModellerApp', ['Catalog'])

        # Adding model 'ModellingResult'
        db.create_table('ModellerApp_modellingresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lens_data_obj', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ModellerApp.LensData'], null=True, blank=True)),
            ('json_str', self.gf('django.db.models.fields.TextField')()),
            ('is_final_result', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('created_by_str', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('rendered_last', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_accessed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_rendered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('local_url', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('n_models', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pixrad', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hubbletime', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('steepness_min', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('steepness_max', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('smooth_val', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('smooth_include_central', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('local_gradient', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('is_symm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('maprad', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('shear', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('redshift_lens', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('redshift_source', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('n_sources', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('n_images', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('log_text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('ModellerApp', ['ModellingResult'])

        # Adding model 'ModellingSession'
        db.create_table('ModellerApp_modellingsession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('basic_data_obj', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ModellerApp.BasicLensData'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ModellerApp.ModellingResult'])),
        ))
        db.send_create_signal('ModellerApp', ['ModellingSession'])


    def backwards(self, orm):
        # Deleting model 'LensData'
        db.delete_table('ModellerApp_lensdata')

        # Deleting model 'Collection'
        db.delete_table('ModellerApp_collection')

        # Removing M2M table for field lenses on 'Collection'
        db.delete_table('ModellerApp_collection_lenses')

        # Deleting model 'BasicLensData'
        db.delete_table('ModellerApp_basiclensdata')

        # Deleting model 'Catalog'
        db.delete_table('ModellerApp_catalog')

        # Deleting model 'ModellingResult'
        db.delete_table('ModellerApp_modellingresult')

        # Deleting model 'ModellingSession'
        db.delete_table('ModellerApp_modellingsession')


    models = {
        'ModellerApp.basiclensdata': {
            'Meta': {'object_name': 'BasicLensData'},
            'catalog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ModellerApp.Catalog']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'catalog_img_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'channel1_data': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel1_imgurl': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'channel1_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'channel2_data': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel2_imgurl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel2_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'channel3_data': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel3_imgurl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel3_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'channel4_data': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel4_imgurl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel4_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'channel5_data': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel5_imgurl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'channel5_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'modellers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['ModellerApp.ModellingSession']", 'symmetrical': 'False'}),
            'n_res': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'requested_last': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'z_lens': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z_source': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'ModellerApp.catalog': {
            'Meta': {'object_name': 'Catalog'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'ModellerApp.collection': {
            'Meta': {'object_name': 'Collection'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'created_by_str': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lenses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ModellerApp.LensData']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'ModellerApp.lensdata': {
            'Meta': {'object_name': 'LensData'},
            'add_data': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'created_by_str': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'datasource': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'datasource_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_data': ('django.db.models.fields.TextField', [], {}),
            'last_accessed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'n_res': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'ModellerApp.modellingresult': {
            'Meta': {'object_name': 'ModellingResult'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'created_by_str': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'hubbletime': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_final_result': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_rendered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_symm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'json_str': ('django.db.models.fields.TextField', [], {}),
            'last_accessed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lens_data_obj': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ModellerApp.LensData']", 'null': 'True', 'blank': 'True'}),
            'local_gradient': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'local_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'log_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'maprad': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'n_images': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'n_models': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'n_sources': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pixrad': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'redshift_lens': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'redshift_source': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rendered_last': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shear': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'smooth_include_central': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'smooth_val': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'steepness_max': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'steepness_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'ModellerApp.modellingsession': {
            'Meta': {'object_name': 'ModellingSession'},
            'basic_data_obj': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ModellerApp.BasicLensData']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ModellerApp.ModellingResult']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['ModellerApp']