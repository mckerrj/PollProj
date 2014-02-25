from django.contrib import admin
from twitter.models import Poll, Choice, Entry, TwitterUser, Tweet


admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Entry)
admin.site.register(TwitterUser)
admin.site.register(Tweet)