## Tests!

### I've written a series of tests just  to show some different, simple test conventions

- The Tests in [test_api.py](https://github.com/mckerrj/TwitterApp/blob/master/twitter/tests/test_api.py) are for testing the Entry and User resources.
  - I'm loading fixture data for testing in this case.  You can see the load at the top in this line <code>fixtures = ['data.json']</code>
  - Note the various <code>reverse</code> for the URL building.  In particular there are a couple of things happening to think about for new TastyPie users:
    - <code>api_dispatch_detail</code> vs <code>api_dispatch_list</code>.  There's almost no docos on these, but basically they are only a little obvious.
      Use them to call a list vs a detailed object!  Build the rest of the URL appropriately.
    - There are two different ways of deserializing objects shown and both are kind of handy.  The first deserializes an entire response object in one go and does the
      comparisons.  It can be somewhat unforgiving which may be good or bad depending on your view of the test.
      ```
      self.assertEqual(self.deserialize(response), {
            'id': self.entry_1.pk,
            'user': '/api/v1/user/{0}/'.format(self.user.pk),
            'title': 'This is the second title',
            'slug': 'this-is-the-second-title',
            'body': 'This is the second body',
            'pub_date': '2014-01-17T00:03:23',
            'resource_uri': '/api/v1/entry/{0}/'.format(self.entry_1.pk)
        })
      ```

      The other breaks them up:
      ```
      self.assertEqual(self.deserialize(response)['objects'][0]['title'], 'Post in a test Post!')
      self.assertEqual(self.deserialize(response)['objects'][0]['body'], 'This is an automated test body')
      self.assertEqual(self.deserialize(response)['objects'][0]['pub_date'], '2011-05-01T22:05:12')
      ```
- The tests in [test_twitter_sync](https://github.com/mckerrj/TwitterApp/blob/master/twitter/tests/test_twitter_sync.py) are using mocks for testing
  This is generally better than fixture data, but now always.  Certainly for this kind of test it is.  You don't want to call the Twitter API on a
  unit test.
  - Basically mock uses a decorator to intercept a method call and substitute the method for another method. Here you can see that the
    <code>@patch...</code> call defines what to do, which is call <code>load_twitter_data</code> instead of the
    <code>twitter.twitter_sync.call_for_timeline_data_json</code> function.  The <code>load_twitter_data() just sets up the mock.
    ```
    def load_twitter_data():
        json_data = open('twitter/tests/fixtures/mocktwitter.json')
        data1 = json.load(json_data)
        return data1

    @patch('twitter.twitter_sync.call_for_timeline_data_json', load_twitter_data)
    def test_get_sync_twitter_user_timeline_getorcreate(self):
        self.data = twitter_sync.call_for_timeline_data_json()
        twitter_sync.sync_tweets_and_users_getorcreate(self.data)
        self.assertEquals(TwitterUser.objects.all().count(), 1)
        self.assertEquals(Tweet.objects.all().count(), 5)
    ```

- The tests in [test_twitter_api.py](https://github.com/mckerrj/TwitterApp/blob/master/twitter/tests/test_twitter_api.py) are mostly similar to the
  tests show in test_api.py, but just a couple of things to note:
  - The <code>assertKeys</code> is pretty handy for testing against JSON.
  ```
  self.assertKeys(self.deserialize(response), ['id', 'lang', 'screen_name', 'resource_uri', 'friends_count', 'profile_image_url_https',
                                               'profile_image_url', 'followers_count', 'id_str', 'name']
  ```
  - You can call the APIs using reverse or a simple URI call.
  ```
  get_entry_url = reverse('api_dispatch_list', kwargs={'resource_name': 'tweet', 'api_name': 'v1'})
  ```
  OR
  ```
  response = self.api_client.get('/api/v1/twitteruser/newtMcKerr/', format='json')
  ```
- Test_basic.py is just the sample tests from the DJango tutorial.