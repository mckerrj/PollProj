from tastypie.test import ResourceTestCase
from requests_oauthlib import OAuth1
import requests
from polls.models import Tweet
import datetime
import pytz
from django.conf import settings

OAUTH_TOKEN = '260431924-oAqZnVPosiGssJMLWTFlpdE1x9Xnc379RmyafpX7'
OAUTH_TOKEN_SECRET = 'wKOyRxjjDiJZMOBJwzcZcc0FZvaEYwjqCBZGHaP1SSlJA'
CONSUMER_KEY = 'qLh1cmWyqZpMWhfWKIHew'
CONSUMER_SECRET = 'JqLTPD1UN5d5Yzev82tBLSexIdMHmRMdlu1Ml9vig'


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=OAUTH_TOKEN,
                   resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth


class TestsTweetResource(ResourceTestCase):
    def setUp(self):
        super(TestsTweetResource, self).setUp()
        print("Setup stage")

    def test_get_something(self):
        oauth = get_oauth()
        response = requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=newtMcKerr", auth=oauth)
        data = response.json()

        # A bunch of random stuff to play with how response works and what data/formats can be had.
        #print(response.encoding)
        #print(response.content)
        #print(response.json())
        #data = simplejson.loads(response.content)
        #print(response.json()[0]['created_at'])

        # todo need to check to make sure the timezone stuff is working right.
        # todo add assertion
        for tweet in range(len(data)):
            print(data[tweet]['created_at'])
            t, created = Tweet.objects.get_or_create(id=data[tweet]['id'],
                                                     id_str=data[tweet]['id_str'],
                                                     text=data[tweet]['text'],
                                                     created_at=datetime.datetime.strptime(data[tweet]['created_at'],
                                                                                           '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.timezone(settings.TIME_ZONE)),
                                                     favorite_count=data[tweet]['favorite_count'],
                                                     favorited=data[tweet]['favorited'], )
            print('Tweet: %s' % t, 'Was Created: %s' % created)
