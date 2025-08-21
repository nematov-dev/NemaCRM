from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from app_page.models import NotificationModel

# class IndexView(View):
#     def get(self,request):
#         return render(request,'index.html')

class NotificationView(LoginRequiredMixin,View):
    def get(self,request):
        messages = NotificationModel.objects.all().order_by("-created_at")
        return render(request,'page/notification.html',{"messages":messages})
