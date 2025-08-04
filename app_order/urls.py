from django.urls import path

from app_order import views

app_name = 'app_order'

urlpatterns = [
    path('order-confirm/',views.ConfirmOrder.as_view(),name="order-confirm")
]