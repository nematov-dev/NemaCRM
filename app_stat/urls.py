from django.urls import path

from app_stat import views

app_name = 'app_stat'

urlpatterns = [
    path('',views.StatView.as_view(),name='stat')
]