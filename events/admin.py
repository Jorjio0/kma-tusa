from django.contrib import admin

from .models import Category, Event, Organizer, Venue

admin.site.register(Category)
admin.site.register(Organizer)
admin.site.register(Venue)
admin.site.register(Event)
