from tastypie.test import ResourceTestCase
from polls import twitter_sync
from polls.models import Tweet, TwitterUser


# todo change to mock objects
class TestsTweetResource(ResourceTestCase):
    def setUp(self):
        super(TestsTweetResource, self).setUp()

    def test_get_sync_twitter_user_timeline(self):
        data = twitter_sync.call_for_timeline_data_json()
        twitter_sync.sync_tweets_and_users(data)
        self.assertEquals(TwitterUser.objects.all().count(), 1)
        self.assertEquals(Tweet.objects.all().count(), 5)

    def test_get_sync_twitter_user_timeline_simple(self):
        data = twitter_sync.call_for_timeline_data_json()
        twitter_sync.sync_tweets_and_users_simplesave(data)
        self.assertEquals(TwitterUser.objects.all().count(), 1)
        self.assertEquals(Tweet.objects.all().count(), 5)
