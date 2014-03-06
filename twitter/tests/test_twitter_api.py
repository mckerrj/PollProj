from tastypie.test import ResourceTestCase
from django.core.urlresolvers import reverse


# Since this app pulls its data through twitter_sync using celery, I'm only doing gets for testing these
# APIs.  I've limited  allowed calls to those methods to 'get' anyway.  For examples on how to call,
# test, deserialize TastyPie API get/put/delete methods look at the tests in test_api.py.
class TestsEntryResource(ResourceTestCase):
    fixtures = ['tweetdata.json']

    def setUp(self):
        super(TestsEntryResource, self).setUp()

    def test_get_tweet_list(self):
        get_entry_url = reverse('api_dispatch_list', kwargs={'resource_name': 'tweet', 'api_name': 'v1'})
        response = self.api_client.get(get_entry_url, format='json')
        self.assertValidJSONResponse(response)
        self.assertEqual(len(self.deserialize(response)['objects']), 5)

    def test_get_twitteruser_detail(self):
        response = self.api_client.get('/api/v1/twitteruser/newtMcKerr/', format='json')
        self.assertValidJSONResponse(response)
        self.assertEqual(self.deserialize(response)['screen_name'], 'newtMckerr')
        self.assertKeys(self.deserialize(response), ['id', 'lang', 'screen_name', 'resource_uri', 'friends_count', 'profile_image_url_https',
                                                     'profile_image_url', 'followers_count', 'id_str', 'name']
        )