from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from app_page.models import NotificationModel,NemaCRMPhonePhotoModel,NemaCRMPCPhotoModel

class IndexView(View):
    def get(self,request):
        phones = NemaCRMPhonePhotoModel.objects.all()
        pc = NemaCRMPCPhotoModel.objects.all()
        context = {
            "phones":phones,
            "pc":pc
        }
        return render(request,'page/index.html',context)

class NotificationView(LoginRequiredMixin,View):
    def get(self,request):
        messages = NotificationModel.objects.all().order_by("-created_at")
        return render(request,'page/notification.html',{"messages":messages})
