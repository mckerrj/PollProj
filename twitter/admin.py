from django.contrib import admin
from twitter.models import Poll, Choice, Entry


admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Entry)