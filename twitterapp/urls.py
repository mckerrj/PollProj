from django.conf.urls import patterns, include, url
from django.contrib import admin
from twitter import views
from twitter.api import EntryResource, UserResource, PollResource, ChoiceResource, TweetResource, TwitterUserResource
from tastypie.api import Api
from django.views.generic import TemplateView

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(EntryResource())
v1_api.register(PollResource())
v1_api.register(ChoiceResource())
v1_api.register(TweetResource())
v1_api.register(TwitterUserResource())


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^twitter/', include('twitterapp.urls', namespace='twitter')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^$', TemplateView.as_view(template_name='twitter_main.html'), name="twmain"),
    url(r'^twuser/$', TemplateView.as_view(template_name='twitter_user.html'), name="twuser"),
    url(r'^twconv/$', TemplateView.as_view(template_name='twitter_conversation.html'), name="twconv"),

)