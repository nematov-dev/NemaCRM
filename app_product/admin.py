from django.contrib import admin

from app_product.models import ProductModel

@admin.register(ProductModel)
class ProductModelModel(admin.ModelAdmin):
    list_display = ('user','name','price','created_at')
    search_fields = ['name']
    list_filter = ['user','category','unity','created_at']
    ordering = ['-created_at']
