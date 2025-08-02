from django.urls import path

from app_dashboard import views

app_name = 'app_dashboard'

urlpatterns = [
    path('',views.Dashboard.as_view(),name='dashboard'),
    path('cart/',views.Cart.as_view(),name='cart')
]