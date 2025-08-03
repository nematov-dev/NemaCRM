from django.urls import path

from app_dashboard import views

app_name = 'app_dashboard'

urlpatterns = [
    path('',views.Dashboard.as_view(),name='dashboard'),
    path('cart/',views.CartView.as_view(),name='cart-list'),
    path('cart-add/<int:product_id>/',views.AddCartView.as_view(),name="cart-add"),
    path('cart-clear/',views.CartClearView.as_view(),name="cart-clear"),
    path('cart-cancel/<int:pk>/',views.CartProductCancel.as_view(),name='cart-cancel')
]