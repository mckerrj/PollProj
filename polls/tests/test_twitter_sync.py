from tastypie.test import ResourceTestCase
from polls import twitter_sync
from polls.models import Tweet, TwitterUser
from mock import patch
import json


def load_twitter_data():
    json_data = open('polls/tests/fixtures/mocktwitter.json')
    data1 = json.load(json_data)
    return data1


# This is for testing the twitter_sync.sync_blah methods.  It's using a simple Mock decorator/
# interceptor to prevent calling the actual API.  It loads data from fixtures/mocktwitter
# that I got using the call_for_timeline_data_json method.  So it should be clean.  If you really
# want, you can comment out the @patch lines and it'll run the tests against actual twitter API.
# Generally not recommended, but good to do for giggles.
# IF YOU DO WANT TO RUN AGAINST TWITTER API, you'll need to change the AUTH_TOKEN, AUTH_TOKEN_SECRET,
# CONSUMER_KEY, CONSUMER_SECRET, and the API_URL to your own stuff.  You'll need a twitter account, and
# all that stuff generated from Twitter's Developer page for your account.
class TestsTweetResource(ResourceTestCase):

    def setUp(self):
        super(TestsTweetResource, self).setUp()

    @patch('polls.twitter_sync.call_for_timeline_data_json', load_twitter_data)
    def test_get_sync_twitter_user_timeline(self):
        self.data = twitter_sync.call_for_timeline_data_json()
        twitter_sync.sync_tweets_and_users(self.data)
        self.assertEquals(TwitterUser.objects.all().count(), 1)
        self.assertEquals(Tweet.objects.all().count(), 5)

    @patch('polls.twitter_sync.call_for_timeline_data_json', load_twitter_data)
    def test_get_sync_twitter_user_timeline_simple(self):
        self.data = twitter_sync.call_for_timeline_data_json()
        twitter_sync.sync_tweets_and_users_simplesave(self.data)
        self.assertEquals(TwitterUser.objects.all().count(), 1)
        self.assertEquals(Tweet.objects.all().count(), 5)
