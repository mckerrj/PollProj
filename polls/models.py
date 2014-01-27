from django.db import models
from django.utils import timezone
import datetime
from tastypie.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.text import slugify
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)


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


