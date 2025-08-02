from django.shortcuts import render
from django.views import View

from app_page.models import NotificationModel

class NotificationView(View):
    def get(self,request):
        messages = NotificationModel.objects.all().order_by("-created_at")
        return render(request,'page/notification.html',{"messages":messages})
