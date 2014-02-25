from __future__ import absolute_import
from twitterapp.celeryapp import app
from twitter import twitter_sync
from twitter.models import Tweet


@app.task
def hello():
    return 'hello world'


@app.task
def add(x, y):
    atuple = (x, y)
    print("Sum of args: %s" % sum(atuple))
    return x + y


@app.task
def run_twitter_sync():
    data = twitter_sync.call_for_timeline_data_json()
    twitter_sync.sync_tweets_and_users_save(data)
    print(Tweet.objects.all())