from __future__ import absolute_import
from PollProj.celeryapp import app
from polls import sync_twitter
from polls.models import Tweet


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
    data = sync_twitter.call_for_data_json(url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=newtMcKerr")
    sync_twitter.sync_tweets_and_users(data)
    print(Tweet.objects.all())

# To run this app go to prod root and, "celery --app=PollProj worker --loglevel=info -B"