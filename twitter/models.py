from django.db import models
from django.utils import timezone
import datetime
from tastypie.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.text import slugify
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)


class TwitterUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_str = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    screen_name = models.CharField(max_length=200)
    followers_count = models.IntegerField()
    friends_count = models.IntegerField()
    profile_image_url = models.CharField(max_length=255)
    profile_image_url_https = models.CharField(max_length=255)
    lang = models.CharField(max_length=200)
    

    def __unicode__(self):
        return u'ID: %s, screen_name: %s' % (self.id_str, self.screen_name)


class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_str = models.CharField(max_length=200)
    twitter_user = models.ForeignKey(TwitterUser)
    text = models.CharField(max_length=400)
    created_at = models.DateTimeField(blank=True, null=True)
    favorite_count = models.IntegerField()
    favorited = models.BooleanField()
    retweet_count = models.IntegerField()
    lang = models.TextField()
    

    def __unicode__(self):
        return u'ID: %s, Text: %s' % (self.id_str, self.text)


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        return timezone.now() > self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text


class Entry(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=now)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    body = models.TextField()

    def __unicode__(self):
        return u'%s : %s' % (self.title, self.slug)

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
        	self.slug = slugify(unicode(self.title))[:50]

        return super(Entry, self).save(*args, **kwargs)