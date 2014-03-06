from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from tastypie import fields
from twitter.models import Entry, Poll, Choice, Tweet, TwitterUser
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
#from happyhour.api.authentication import MultiAuthentication, BouncerCookieAuthentication, MultipleValueTwoLeggedOAuthAuthentication
from django.conf.urls import url


# Pretty standard resource.  Kept to show that you can white list fields, or exclude them
# or whitelist them.  Also easy to restrict callable methods for the REST api.
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password']  # Excludes fields
        #  fields = ['email', 'password']  # white list of fields style
        allowed_methods = ['get']
        filtering = {
            'username': ALL,
        }
        #authorization = Authorization()
        #authentication = MultiAuthentication(MultipleValueTwoLeggedOAuthAuthentication(), BouncerCookieAuthentication())


# Entry shows basic relationship and some more filtering options.
# Relationship shows path to related object.
class EntryResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'slug': ALL,
        }
        authorization = Authorization()
        #authentication = MultiAuthentication(MultipleValueTwoLeggedOAuthAuthentication(), BouncerCookieAuthentication())


# Basic Poll, nothing to see here.
class PollResource(ModelResource):
    class Meta:
        queryset = Poll.objects.all()
        resource_name = 'poll'
        always_return_date = True
        filtering = {
            'question': ALL,
        }


# Choice is pretty standard, I added full=True to the relationship to show sample data returned
# that includes fully instantiated relationships.  The API will return a choice and it's related Poll.
class ChoiceResource(ModelResource):
    poll = fields.ToOneField(PollResource, 'poll', full=True)

    class Meta:
        queryset = Choice.objects.all()
        resource_name = 'choice'
        always_return_date = True
        filtering = {
            'poll': ALL_WITH_RELATIONS,
            'choice_text': ALL,
        }


# - resource_name will be mapped to the url, so you'll be hitting
#   /api/v1/twitteruser
#   Adding this note to show that it's NOT the same as field mapping (seen below in TweerResource in the FK reference
# - Since data should get pulled from twitter, only method allowed is ['get']
# - The prepend_urls function shows how to modify the URL.  So to get a specific TwitterUserResource
#   you can now call api/v1/twitteruser/<screen_name>/
class TwitterUserResource(ModelResource):
    class Meta:
        queryset = TwitterUser.objects.all()
        resource_name = 'twitteruser'
        allowed_methods = ['get']
        detail_uri_name = 'screen_name'

        def prepend_urls(self):
            return [
                url(r"^(?P<resource_name>%s)/(?P<screen_name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            ]


class TweetResource(ModelResource):
    twitteruser = fields.ToOneField(TwitterUserResource, 'twitter_user', full=True)

    class Meta:
        queryset = Tweet.objects.all()
        resource_name = 'tweet'
        allowed_methods = ['get']
        filtering = {
            'twitter_user': ALL_WITH_RELATIONS,
        }