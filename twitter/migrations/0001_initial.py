# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TwitterUser'
        db.create_table(u'twitter_twitteruser', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('id_str', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('followers_count', self.gf('django.db.models.fields.IntegerField')()),
            ('friends_count', self.gf('django.db.models.fields.IntegerField')()),
            ('profile_image_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('profile_image_url_https', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'twitter', ['TwitterUser'])

        # Adding model 'Tweet'
        db.create_table(u'twitter_tweet', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('id_str', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('twitter_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitter.TwitterUser'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('favorite_count', self.gf('django.db.models.fields.IntegerField')()),
            ('favorited', self.gf('django.db.models.fields.BooleanField')()),
            ('retweet_count', self.gf('django.db.models.fields.IntegerField')()),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'twitter', ['Tweet'])

        # Adding model 'Poll'
        db.create_table(u'twitter_poll', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'twitter', ['Poll'])

        # Adding model 'Choice'
        db.create_table(u'twitter_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitter.Poll'])),
            ('choice_text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'twitter', ['Choice'])

        # Adding model 'Entry'
        db.create_table(u'twitter_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 10, 0, 0))),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'twitter', ['Entry'])


    def backwards(self, orm):
        # Deleting model 'TwitterUser'
        db.delete_table(u'twitter_twitteruser')

        # Deleting model 'Tweet'
        db.delete_table(u'twitter_tweet')

        # Deleting model 'Poll'
        db.delete_table(u'twitter_poll')

        # Deleting model 'Choice'
        db.delete_table(u'twitter_choice')

        # Deleting model 'Entry'
        db.delete_table(u'twitter_entry')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'twitter.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['twitter.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'twitter.entry': {
            'Meta': {'object_name': 'Entry'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 10, 0, 0)'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'twitter.poll': {
            'Meta': {'object_name': 'Poll'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'twitter.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'favorite_count': ('django.db.models.fields.IntegerField', [], {}),
            'favorited': ('django.db.models.fields.BooleanField', [], {}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'id_str': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'retweet_count': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'twitter_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['twitter.TwitterUser']"})
        },
        u'twitter.twitteruser': {
            'Meta': {'object_name': 'TwitterUser'},
            'followers_count': ('django.db.models.fields.IntegerField', [], {}),
            'friends_count': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'id_str': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'profile_image_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'profile_image_url_https': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['twitter']