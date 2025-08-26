from django.urls import path

from app_auth import views

app_name = 'app_auth'

urlpatterns = [
    path('email/', views.phone_view, name='phone'),
    path('verify/', views.verify_view, name='verify'),
    path('register/', views.RegisterView.as_view(), name='register'),    
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('password-forget/',views.ForgetPasswordView.as_view(),name='password-forget'),
    path('password-forget-confirm/',views.ForgetPasswordConfimView.as_view(),name='password-forget-confirm'),
    path('password-forget-done/',views.ForgetPasswordDone.as_view(),name='password-forget-done'),

]