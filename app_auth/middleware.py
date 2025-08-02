from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import logout

class SubscriptionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            profile = getattr(user, 'profile', None)
            if profile and profile.subscription:
                if profile.subscription < timezone.now():
                    if user.is_active:
                        user.is_active = False
                        user.save()
                        logout(request) 
                        return redirect('app_auth:login')
        return self.get_response(request)
