from requests_oauthlib import OAuth1
import requests
from polls.models import Tweet, TwitterUser
import datetime
import pytz

OAUTH_TOKEN = '260431924-oAqZnVPosiGssJMLWTFlpdE1x9Xnc379RmyafpX7'
OAUTH_TOKEN_SECRET = 'wKOyRxjjDiJZMOBJwzcZcc0FZvaEYwjqCBZGHaP1SSlJA'
CONSUMER_KEY = 'qLh1cmWyqZpMWhfWKIHew'
CONSUMER_SECRET = 'JqLTPD1UN5d5Yzev82tBLSexIdMHmRMdlu1Ml9vig'
API_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=newtMcKerr'


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=OAUTH_TOKEN,
                   resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth


# todo add exception handling?
def call_for_timeline_data_json():
    oauth = get_oauth()
    response = requests.get(url=API_URL, auth=oauth)
    # A bunch of random stuff to play with how response works and what data/formats can be retrieved.
    #print(response.encoding)
    #print(response.content)
    #print(response.json())
    #data = simplejson.loads(response.content)
    return response.json()


# get_or_create seems obvious, but short circuits if exists.  Keeping this here because
# it shows the get_or_create method with returns a tuple (not show) of the object and a boolean.
# You'd use this if you DID NOT want to update changes to existing tweets or users.
def sync_tweets_and_users_getorcreate(data):
    for tweet in range(len(data)):
        tu_fields = {'id_str': data[tweet]['user']['id_str'],
                     'name': data[tweet]['user']['name'],
                     'screen_name': data[tweet]['user']['screen_name'],
                     'followers_count': data[tweet]['user']['followers_count'],
                     'friends_count': data[tweet]['user']['friends_count'],
                     'profile_image_url': data[tweet]['user']['profile_image_url'],
                     'profile_image_url_https': data[tweet]['user']['profile_image_url_https'],
                     'lang': data[tweet]['user']['lang']
                    }
        TwitterUser.objects.get_or_create(id=data[tweet]['user']['id'], defaults=tu_fields)

        t_fields = {'id_str': data[tweet]['id_str'],
                    'twitter_user_id': data[tweet]['user']['id'],
                    'text': data[tweet]['text'],
                    'created_at': datetime.datetime.strptime(data[tweet]['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.utc),
                    'favorite_count': data[tweet]['favorite_count'],
                    'favorited': data[tweet]['favorited'],
                    'retweet_count': data[tweet]['retweet_count'],
                    'lang': data[tweet]['lang'],
                    }
        Tweet.objects.get_or_create(id=data[tweet]['id'], defaults=t_fields)


# This works gracefully too, but is effectively updating user if any changes.
# After 1.5, it'll update fields.
def sync_tweets_and_users_save(data):
    for tweet in range(len(data)):
        tu = TwitterUser(id=data[tweet]['user']['id'],
                         name=data[tweet]['user']['name'],
                         screen_name=data[tweet]['user']['screen_name'],
                         followers_count=data[tweet]['user']['followers_count'],
                         friends_count=data[tweet]['user']['friends_count'],
                         profile_image_url=data[tweet]['user']['profile_image_url'],
                         profile_image_url_https=data[tweet]['user']['profile_image_url_https'],
                         lang=data[tweet]['user']['lang']
                         )
        tu.save()

        t = Tweet(id=data[tweet]['id'],
                  twitter_user_id=data[tweet]['user']['id'],
                  text=data[tweet]['text'],
                  created_at=datetime.datetime.strptime(data[tweet]['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.utc),
                  favorite_count=data[tweet]['favorite_count'],
                  favorited=data[tweet]['favorited'],
                  retweet_count=data[tweet]['retweet_count'],
                  lang=data[tweet]['lang']
                  )
        t.save()