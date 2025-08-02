from django.shortcuts import render
from django.views import View

class StatView(View):
    def get(self,request):
        return render(request,'stat/stat.html')
