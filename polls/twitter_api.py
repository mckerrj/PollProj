from polls.models import Tweet
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


class TweetResource(ModelResource):
    class Meta:
        queryset = Tweet.objects.all()
        resource_name = 'tweet'