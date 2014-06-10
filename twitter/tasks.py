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
    try:
        data = twitter_sync.call_for_timeline_data_json()
        twitter_sync.sync_tweets_and_users_save(data)
        #print(Tweet.objects.all())
    except Exception as e:
    	print(e)
        print("There was an error either connecting to Twitter API or syncing data. Check your security and screen_name info in settings.py: %s" % e)
