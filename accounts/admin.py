from django.contrib import admin
from .models import UserAccount
from django.contrib.auth.admin import UserAdmin
admin.site.register(UserAccount)
