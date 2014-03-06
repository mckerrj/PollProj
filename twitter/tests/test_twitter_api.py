from tastypie.test import ResourceTestCase
from django.core.urlresolvers import reverse
#from tastypie_two_legged_oauth.models import OAuthConsumer
#from happyhour.api.clients import oauth2_wrap


# Since this app pulls its data through twitter_sync using celery, I'm only doing gets for testing these
# APIs.  I've limited  allowed calls to those methods to 'get' anyway.  For examples on how to call,
# test, deserialize TastyPie API get/put/delete methods look at the tests in test_api.py.
class TestsEntryResource(ResourceTestCase):
    fixtures = ['tweetdata.json']

    def setUp(self):
        super(TestsEntryResource, self).setUp()

        # Create oauth stuff
        #self.consumer = OAuthConsumer.objects.create(name='Test', key='foo', secret='bar')

    # Showing how to do the basic get from the resource, and test to make sure it is secured.
    # def test_get_tweet_unauthorized(self):
    #     self.assertHttpUnauthorized(self.api_client.get('/api/v1/tweet/', format='json'))
    #
    # # This does exactly the same as the previous test, but uses DJango's reverse mechanism to build the URL  Just showing two different
    # # ways of doing it.
    # def test_get_tweet_reverse_unauthorized(self):
    #     self.assertHttpUnauthorized(self.api_client.get(reverse('api_dispatch_list', kwargs={'resource_name': 'tweet', 'api_name': 'v1'})))
    #
    # def test_get_twitteruser_unauthorized(self):
    #     self.assertHttpUnauthorized(self.api_client.get(reverse('api_dispatch_list', kwargs={'resource_name': 'twitteruser', 'api_name': 'v1'})))

    def test_get_tweet_list(self):
        get_entry_url = reverse('api_dispatch_list', kwargs={'resource_name': 'tweet', 'api_name': 'v1'})
        wrapped_url = oauth2_wrap(get_entry_url, 'foo', 'bar')
        response = self.api_client.get(wrapped_url, format='json')
        self.assertValidJSONResponse(response)
        self.assertEqual(len(self.deserialize(response)['objects']), 5)

    def test_get_twitteruser_detail(self):
        wrapped_url = oauth2_wrap('/api/v1/twitteruser/newtMcKerr/', 'foo', 'bar')
        response = self.api_client.get(wrapped_url, format='json')
        self.assertValidJSONResponse(response)
        self.assertEqual(self.deserialize(response)['screen_name'], 'newtMckerr')
        self.assertKeys(self.deserialize(response), ['id', 'lang', 'screen_name', 'resource_uri', 'friends_count', 'profile_image_url_https',
                                                     'profile_image_url', 'followers_count', 'id_str', 'name']
        )