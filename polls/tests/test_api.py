from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from polls.models import Entry
from tastypie_two_legged_oauth.models import OAuthConsumer
from django.core.urlresolvers import reverse
from happyhour.api.clients import oauth2_wrap
import urllib
import datetime


class TestsEntryResource(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['data.json']

    def setUp(self):
        super(TestsEntryResource, self).setUp()

        # Create a user.
        self.username = 'mckerrj'
        self.user = User.objects.get(username=self.username)
        self.consumer = OAuthConsumer.objects.create(name='Test', key='foo', secret='bar')

        # Fetch the ``Entry`` object we'll use in testing.
        # Note that we aren't using PKs because they can change depending
        # on what other tests are running.
        self.entry_1 = Entry.objects.get(slug='this-is-the-second-title')

        # The data we'll send on POST requests. Again, because we'll use it
        # frequently (enough).
        self.post_data = {
            'user': '/api/v1/user/{0}/'.format(self.user.pk),
            'title': 'Post in a test Post!',
            'body': 'This is an automated test body',
            'pub_date': '2011-05-01T22:05:12'
        }

    def test_get_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/user/', format='json'))

    # Done a different way just for giggles.  More abstract, more complex than above.
    def test_get_list__entry_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(reverse('api_dispatch_list', kwargs={'resource_name': 'entry', 'api_name': 'v1'})))


    def test_working_case_user_list(self):
        get_user_url = reverse('api_dispatch_list', kwargs={'resource_name': 'user', 'api_name': 'v1'})
        wrapped_url = oauth2_wrap(get_user_url, 'foo', 'bar')
        response = self.api_client.get(wrapped_url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertValidJSONResponse(response)

    def test_working_case_user_entry(self):
        get_user_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'user', 'api_name': 'v1', 'pk': self.user.pk})
        wrapped_url = oauth2_wrap(get_user_url, 'foo', 'bar')
        response = self.api_client.get(wrapped_url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertValidJSONResponse(response)

    def test_get_list_entry_json(self):
        get_user_url = reverse('api_dispatch_list', kwargs={'resource_name': 'entry', 'api_name': 'v1'})
        wrapped_url = oauth2_wrap(get_user_url, 'foo', 'bar')
        response = self.api_client.get(wrapped_url, format='json')
        self.assertValidJSONResponse(response)
        self.assertEqual(len(self.deserialize(response)['objects']), 5)
        self.assertEqual(self.deserialize(response)['objects'][1], {
            'id': self.entry_1.pk,
            'user': '/api/v1/user/{0}/'.format(self.user.pk),
            'title': 'This is the second title',
            'slug': 'this-is-the-second-title',
            'body': 'This is the second body',
            'pub_date': '2014-01-17T00:03:23',
            'resource_uri': '/api/v1/entry/{0}/'.format(self.entry_1.pk)
        })

    def test_get_entry_json(self):
        get_user_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'entry', 'api_name': 'v1', 'pk': self.entry_1.pk})
        wrapped_url = oauth2_wrap(get_user_url, 'foo', 'bar')
        response = self.api_client.get(wrapped_url, format='json')
        self.assertValidJSONResponse(response)
        self.assertKeys(self.deserialize(response), ['id', 'user', 'pub_date', 'title', 'slug', 'body', 'resource_uri'])
        self.assertEqual(self.deserialize(response)['title'], 'This is the second title')
        # I know, doing it twice, but different methods for my own edification
        self.assertEqual(self.deserialize(response), {
            'id': self.entry_1.pk,
            'user': '/api/v1/user/{0}/'.format(self.user.pk),
            'title': 'This is the second title',
            'slug': 'this-is-the-second-title',
            'body': 'This is the second body',
            'pub_date': '2014-01-17T00:03:23',
            'resource_uri': '/api/v1/entry/{0}/'.format(self.entry_1.pk)
        })

    def test_post_entry_list(self):
        self.assertEqual(Entry.objects.count(), 5)
        get_user_url = reverse('api_dispatch_list', kwargs={'resource_name': 'entry', 'api_name': 'v1'})
        wrapped_url = oauth2_wrap(get_user_url, 'foo', 'bar', method='POST')
        self.api_client.post(wrapped_url, format='json', data=self.post_data)
        self.assertEqual(Entry.objects.count(), 6)

        get_user_url = reverse('api_dispatch_list', kwargs={'resource_name': 'entry', 'api_name': 'v1'})
        params = {'slug': 'post-in-a-test-post'}
        wrapped_url = oauth2_wrap('%s?%s' % (get_user_url, urllib.urlencode(params)), 'foo', 'bar', method='GET')
        response = self.api_client.get(wrapped_url, format='json')
        self.assertEqual(self.deserialize(response)['objects'][0]['title'], 'Post in a test Post!')
        self.assertEqual(self.deserialize(response)['objects'][0]['body'], 'This is an automated test body')
        self.assertEqual(self.deserialize(response)['objects'][0]['pub_date'], '2011-05-01T22:05:12')

    # def test_put_detail(self):
    #     # Grab the current data & modify it slightly.
    #     original_data = self.deserialize(self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials()))
    #     new_data = original_data.copy()
    #     new_data['title'] = 'Updated: First Post'
    #     new_data['created'] = '2012-05-01T20:06:12'
    #
    #     self.assertEqual(Entry.objects.count(), 5)
    #     self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data, authentication=self.get_credentials()))
    #     # Make sure the count hasn't changed & we did an update.
    #     self.assertEqual(Entry.objects.count(), 5)
    #     # Check for updated data.
    #     self.assertEqual(Entry.objects.get(pk=25).title, 'Updated: First Post')
    #     self.assertEqual(Entry.objects.get(pk=25).slug, 'first-post')
    #     self.assertEqual(Entry.objects.get(pk=25).created, datetime.datetime(2012, 3, 1, 13, 6, 12))


        # def test_delete_detail_unauthenticated(self):
        #     self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))
        #
        # def test_delete_detail(self):
        #     self.assertEqual(Entry.objects.count(), 5)
        #     self.assertHttpAccepted(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))
        #     self.assertEqual(Entry.objects.count(), 4)