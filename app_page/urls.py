from django.urls import path

from app_page import views

app_name = "app_page"

urlpatterns = [
    path('notification/',views.NotificationView.as_view(),name='notification'),
    # path('',views.IndexView.as_view(),name='index')
]