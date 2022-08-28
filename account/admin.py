from django.contrib import admin

from .models import CustomUser
from account.models import CustomUser
# Register your models here.
admin.site.register(CustomUser)
