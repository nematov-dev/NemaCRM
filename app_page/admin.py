from django.contrib import admin

from app_page.models import NotificationModel

@admin.register(NotificationModel)
class NotificationModelAdmin(admin.ModelAdmin):
    list_display = ('message','created_at')
    search_fields = ['message']
    list_filter = ['created_at']
    ordering = ['-created_at']

