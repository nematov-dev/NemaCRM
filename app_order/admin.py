from django.contrib import admin

from app_order.models import OrderModel

@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('user','product','price','created_at')
    search_fields = ['product']
    list_filter = ['user','created_at','product']
    ordering = ['-created_at']
