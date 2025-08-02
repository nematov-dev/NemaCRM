from django.contrib import admin

from app_category.models import CategoryModel

@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('user','name','created_at')
    search_fields = ['name']
    list_filter = ['user','created_at']
    ordering = ['-created_at']