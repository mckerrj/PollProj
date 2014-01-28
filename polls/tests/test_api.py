from django.test import TestCase, Client
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from polls.models import Entry
from tastypie_two_legged_oauth.models import OAuthConsumer
from django.core.urlresolvers import reverse
from happyhour.api.clients import oauth2_wrap


class TestsEntryResource(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    fixtures = ['data.json']

    def setUp(self):
        super(TestsEntryResource, self).setUp()

        # Create a user.
        self.username = 'mckerrj'
        #self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.user = User.objects.get(username=self.username)
        self.consumer = OAuthConsumer.objects.create(name='Test', key='foo', secret='bar')


        # Fetch the ``Entry`` object we'll use in testing.
        # Note that we aren't using PKs because they can change depending
        # on what other tests are running.
        self.entry_1 = Entry.objects.get(slug='this-is-the-second-title')


        # We also build a detail URI, since we will be using it all over.
        # DRY, baby. DRY.
        #self.detail_url = '/api/v1/entry/{0}/'.format(self.entry_1.pk)

        # The data we'll send on POST requests. Again, because we'll use it
        # frequently (enough).
        # self.post_data = {
        #     'user': '/api/v1/user/{0}/'.format(self.user.pk),
        #     'title': 'Second Post!',
        #     'slug': 'second-post',
        #     'created': '2012-05-01T22:05:12'
        # }

    def test_get_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/user/', format='json'))

    def test_working_case(self):
        client = Client()
        get_user_url = reverse('api_dispatch_list', kwargs={'resource_name': 'user', 'api_name': 'v1'})
        wrapped_url = oauth2_wrap(get_user_url, 'foo', 'bar')
        response = client.get(wrapped_url)
        self.assertEqual(response.status_code, 200)

    def test_get_list_json(self):
        resp = self.api_client.get(oauth2_wrap('/api/v1/entry/', 'foo', 'bar'))
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 5)
        self.assertEqual(self.deserialize(resp)['objects'][1], {
            'id': int(str(self.entry_1.pk)),
            'user': '/api/v1/user/{0}/'.format(self.user.pk),
            'title': 'This is the second title',
            'slug': 'this-is-the-second-title',
            'body': 'This is the second body',
            'pub_date': '2014-01-17T00:03:23',
            'resource_uri': '/api/v1/entry/{0}/'.format(self.entry_1.pk)
        })
        #
        # def test_get_list_xml(self):
        #     self.assertValidXMLResponse(self.api_client.get('/api/v1/entries/', format='xml', authentication=self.get_credentials()))
        #
        # def test_get_detail_unauthenticated(self):
        #     self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))
        #
        # def test_get_detail_json(self):
        #     resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        #     self.assertValidJSONResponse(resp)
        #
        #     # We use ``assertKeys`` here to just verify the keys, not all the data.
        #     self.assertKeys(self.deserialize(resp), ['created', 'slug', 'title', 'user'])
        #     self.assertEqual(self.deserialize(resp)['name'], 'First post')
        #
        # def test_get_detail_xml(self):
        #     self.assertValidXMLResponse(self.api_client.get(self.detail_url, format='xml', authentication=self.get_credentials()))
        #
        # def test_post_list_unauthenticated(self):
        #     self.assertHttpUnauthorized(self.api_client.post('/api/v1/entries/', format='json', data=self.post_data))
        #
        # def test_post_list(self):
        #     # Check how many are there first.
        #     self.assertEqual(Entry.objects.count(), 5)
        #     self.assertHttpCreated(self.api_client.post('/api/v1/entries/', format='json', data=self.post_data, authentication=self.get_credentials()))
        #     # Verify a new one has been added.
        #     self.assertEqual(Entry.objects.count(), 6)
        #
        # def test_put_detail_unauthenticated(self):
        #     self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))
        #
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
        #
        # def test_delete_detail_unauthenticated(self):
        #     self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))
        #
        # def test_delete_detail(self):
        #     self.assertEqual(Entry.objects.count(), 5)
        #     self.assertHttpAccepted(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))
        #     self.assertEqual(Entry.objects.count(), 4)