from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password

from app_auth import forms

User = get_user_model()

class LoginView(View):
    def get(self,request):
        form = forms.LoginForm()
        return render(request,'auth/signin.html',{"form":form})
    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()

            if user:
                if not user.is_active:
                    form.add_error(None, "Sizning obunangiz muddati tugagan! Admin bilan bo'glaning.")
                elif check_password(password, user.password):
                    login(request, user)
                    return redirect('app_dashboard:dashboard')
                else:
                    form.add_error(None, "Username yoki parol notug'ri!")
            else:
                form.add_error(None, "Username yoki parol notug'ri!")
        else:
            form.add_error(None, "Formani to‘ldiring!")
        return render(request, 'auth/signin.html', {'form': form})
        
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("app_auth:login")

class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        profile_form = forms.ProfileForm()
        return render(request,'auth/profile.html',{"profile_form":profile_form})
    
    def post(self,request):
        if "profile_submit" in request.POST:
            profile_form = forms.ProfileForm(request.POST, request.FILES)
            if profile_form.is_valid():
                image = profile_form.cleaned_data['image']
                fullname = profile_form.cleaned_data['fullname']
                phone = profile_form.cleaned_data['phone']
                username = profile_form.cleaned_data['username']

                user = request.user

                if username:
                    user.username = username
                if fullname:
                    user.first_name = fullname
                if image:
                    user.profile.image = image
                if phone:
                    user.profile.phone = phone

                user.save()
                user.profile.save()
                messages.success(request, "Ma'lumotlaringiz yangilandi.")
                return redirect('app_auth:profile')
            else:
                messages.error(request, "Formani to‘ldiring!")
            return render(request,'auth/profile.html',{"profile_form":profile_form})
        
        elif "password_submit" in request.POST:
            password_form = forms.ChangePasswordForm(request.POST)
            if password_form.is_valid():
                old_password = password_form.cleaned_data.get('old_password')
                new_password2 = password_form.cleaned_data.get('new_password2')
                user = request.user
                if user.check_password(old_password):
                    user.set_password(new_password2)
                    user.save()
                    messages.success(request,"Parolingiz o'zgartirildi!")
                    update_session_auth_hash(request,user)
                    return redirect('app_auth:profile')
                else:
                    messages.error(request,"Eski parolingiz xato!")
                    return redirect('app_auth:profile')
            else:
                messages.error(request,f"{password_form.errors}")
                
            return render(request,"auth/profile.html",{"password_form":password_form})
        