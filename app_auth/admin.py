from django.contrib import admin

from app_auth.models import ProfileModel

@admin.register(ProfileModel)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user','subscription','created_at')
    search_fields = ['phone']
    list_filter = ['user','subscription','created_at']
    ordering = ['-created_at']

