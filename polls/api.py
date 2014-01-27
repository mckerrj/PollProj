from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization, Authorization
from django.contrib.auth.models import User
from tastypie import fields
from polls.models import Entry, Poll, Choice
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
# from tastypie.authentication import ApiKeyAuthentication
from authentication import OAuth20Authentication


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


class EntryResource(ModelResource):
    #user = fields.ForeignKey(UserResource, 'user')
    # toOne with full=True loads related fields at runtime rather than linking
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        #authorization = DjangoAuthorization()
        #authentication = OAuth20Authentication()


class PollResource(ModelResource):
    class Meta:
        queryset = Poll.objects.all()
        resource_name = 'poll'
        always_return_date = True
        filtering = {
            'question': ALL,
        }
        authorization = Authorization()
        #authorization = DjangoAuthorization()
        #authentication = OAuth20Authentication()


class ChoiceResource(ModelResource):
    poll = fields.ToOneField(PollResource, 'poll', full=True)

    class Meta:
        queryset = Choice.objects.all();
        resource_name = 'choice'
        always_return_date = True
        filtering = {
            'poll': ALL_WITH_RELATIONS,
            'choice_text': ALL,
        }


