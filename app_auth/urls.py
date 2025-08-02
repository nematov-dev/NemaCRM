from django.urls import path

from app_auth import views

app_name = 'app_auth'

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
]