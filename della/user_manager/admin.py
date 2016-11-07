from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ['user', 'is_enabled_exchange']


admin.site.register(UserProfile, UserProfileAdmin)
