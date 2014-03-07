## Celery
I'm using celery to manage scheduled tasks.  There are a couple of sample tasks, just to show how it works,
but the important one calls the Twitter "timeline" api, and sucks up any tweets for the particular
screen name's Twitter account.  It then serializes the returned JSON objects to Python/Django model objects
and stores them.

###Sync the data
- The linked [file](https://github.com/mckerrj/TwitterApp/blob/master/twitter/twitter_sync.py) is the python
  file that syncs the data.  It does the following:
  - Manage the OAuth request.
  - call the timeline URI/REST-API.  Ensre that the response is JSON data.
  - Loop through the collection of data in the JSON object and set the fields for storage.
  - Format data where necessary (dates), and set the timezone.
  - Store the data.
  - I've given two sample ways to do it, both roughly the same but using different Django storage conventions
  - This app uses the <code>sync_tweets_and_users_save(data):</code> method because I want things updated if changed.

###How does celery do it:
- The [celeryapp.py](https://github.com/mckerrj/TwitterApp/blob/master/twitterapp/celeryapp.py) file
  basically gives celery the key settings it needs.

- The [tasks.py] file is the list of programmatic tasks have Celery manage. There are some other samples
  in the file, but the important one is:
  ```
  @app.task
  def run_twitter_sync():
      data = twitter_sync.call_for_timeline_data_json()
      twitter_sync.sync_tweets_and_users_save(data)
      print(Tweet.objects.all())
  ```

  The decorator <code>@app.task</code> registers the task with celery, so it knows what to do. the rest
  is just running the sync.  I should probably collaps the method call, but this is easier to read.
  Print just prints to the console so you can see when the task has happened and see the actual data
  events when you're running celery from the command line.

### Where to manage the tasks:
You manage the tasks in the Django settings file settings.py.
```
  CELERYBEAT_SCHEDULE = {
      'add-every-30-seconds': {
          'task': 'twitter.tasks.add',
          'schedule': timedelta(seconds=30),
          'args': (16, 16)
      },
      'hello-every-10-seconds': {
          'task': 'twitter.tasks.hello',
          'schedule': timedelta(seconds=10)
      },
      'run-twitter-sync-every-5-minutes': {
          'task': 'twitter.tasks.run_twitter_sync',
          'schedule': crontab(minute='*/5')
      },
  }
```

You can see that you can use Celery's syntax or crontab style syntax.
