# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from lbforum.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'LBForumUserProfile'
        db.create_table('lbforum_lbforumuserprofile', (
            ('id', orm['lbforum.LBForumUserProfile:id']),
            ('user', orm['lbforum.LBForumUserProfile:user']),
            ('last_activity', orm['lbforum.LBForumUserProfile:last_activity']),
            ('userrank', orm['lbforum.LBForumUserProfile:userrank']),
            ('last_posttime', orm['lbforum.LBForumUserProfile:last_posttime']),
            ('signature', orm['lbforum.LBForumUserProfile:signature']),
        ))
        db.send_create_signal('lbforum', ['LBForumUserProfile'])
        
        # Adding model 'Topic'
        db.create_table('lbforum_topic', (
            ('id', orm['lbforum.Topic:id']),
            ('forum', orm['lbforum.Topic:forum']),
            ('posted_by', orm['lbforum.Topic:posted_by']),
            ('subject', orm['lbforum.Topic:subject']),
            ('num_views', orm['lbforum.Topic:num_views']),
            ('num_replies', orm['lbforum.Topic:num_replies']),
            ('created_on', orm['lbforum.Topic:created_on']),
            ('updated_on', orm['lbforum.Topic:updated_on']),
            ('last_post', orm['lbforum.Topic:last_post']),
            ('closed', orm['lbforum.Topic:closed']),
            ('sticky', orm['lbforum.Topic:sticky']),
            ('hidden', orm['lbforum.Topic:hidden']),
        ))
        db.send_create_signal('lbforum', ['Topic'])
        
        # Adding model 'Config'
        db.create_table('lbforum_config', (
            ('id', orm['lbforum.Config:id']),
            ('key', orm['lbforum.Config:key']),
            ('value', orm['lbforum.Config:value']),
        ))
        db.send_create_signal('lbforum', ['Config'])
        
        # Adding model 'Post'
        db.create_table('lbforum_post', (
            ('id', orm['lbforum.Post:id']),
            ('topic', orm['lbforum.Post:topic']),
            ('posted_by', orm['lbforum.Post:posted_by']),
            ('poster_ip', orm['lbforum.Post:poster_ip']),
            ('message', orm['lbforum.Post:message']),
            ('created_on', orm['lbforum.Post:created_on']),
            ('updated_on', orm['lbforum.Post:updated_on']),
            ('edited_by', orm['lbforum.Post:edited_by']),
        ))
        db.send_create_signal('lbforum', ['Post'])
        
        # Adding model 'Forum'
        db.create_table('lbforum_forum', (
            ('id', orm['lbforum.Forum:id']),
            ('name', orm['lbforum.Forum:name']),
            ('slug', orm['lbforum.Forum:slug']),
            ('description', orm['lbforum.Forum:description']),
            ('ordering', orm['lbforum.Forum:ordering']),
            ('category', orm['lbforum.Forum:category']),
            ('created_on', orm['lbforum.Forum:created_on']),
            ('updated_on', orm['lbforum.Forum:updated_on']),
            ('num_topics', orm['lbforum.Forum:num_topics']),
            ('num_posts', orm['lbforum.Forum:num_posts']),
            ('last_post', orm['lbforum.Forum:last_post']),
        ))
        db.send_create_signal('lbforum', ['Forum'])
        
        # Adding model 'Category'
        db.create_table('lbforum_category', (
            ('id', orm['lbforum.Category:id']),
            ('name', orm['lbforum.Category:name']),
            ('description', orm['lbforum.Category:description']),
            ('ordering', orm['lbforum.Category:ordering']),
            ('created_on', orm['lbforum.Category:created_on']),
            ('updated_on', orm['lbforum.Category:updated_on']),
        ))
        db.send_create_signal('lbforum', ['Category'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'LBForumUserProfile'
        db.delete_table('lbforum_lbforumuserprofile')
        
        # Deleting model 'Topic'
        db.delete_table('lbforum_topic')
        
        # Deleting model 'Config'
        db.delete_table('lbforum_config')
        
        # Deleting model 'Post'
        db.delete_table('lbforum_post')
        
        # Deleting model 'Forum'
        db.delete_table('lbforum_forum')
        
        # Deleting model 'Category'
        db.delete_table('lbforum_category')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lbforum.category': {
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'lbforum.config': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'lbforum.forum': {
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lbforum.Category']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'num_posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_topics': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '110', 'db_index': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'lbforum.lbforumuserprofile': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_activity': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_posttime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'signature': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'lbforum_profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'userrank': ('django.db.models.fields.CharField', [], {'default': "u'Junior Member'", 'max_length': '30'})
        },
        'lbforum.post': {
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edited_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'poster_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lbforum.Topic']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'lbforum.topic': {
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lbforum.Forum']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'num_replies': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'num_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '999'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['lbforum']
