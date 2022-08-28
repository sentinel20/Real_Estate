from django.contrib import admin

from .models import Listing, Comment

admin.site.register(Listing)
admin.site.register(Comment)
