from datetime import date,timedelta
import random

from django.shortcuts import render,redirect
from django.views import View
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.core.cache import cache

from app_auth import forms

User = get_user_model()

today_date = date.today()
day = today_date + timedelta(days=2)

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
                    form.add_error(None, "Telefon raqam yoki parol notug'ri!")
            else:
                form.add_error(None, "Telefon raqam yoki parol notug'ri!")
        else:
            form.add_error(None, "Formani to‘ldiring!")
        return render(request, 'auth/signin.html', {'form': form})
    
def phone_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if not User.objects.filter(username=phone).exists():
            code = str(random.randint(1000, 9999))
            cache.set(phone, code, timeout=300)  # 5 daqiqa
            # SMS jo‘natish logikasi shu yerga yoziladi
            print(f"Kod: {code}") 
            request.session['phone'] = phone
            return redirect('app_auth:verify')
        else:
            messages.error(request,"Bu telefon raqam bilan foydalanuvchi allaqachon mavjud.")
    return render(request, 'auth/phone.html')

def verify_view(request):
    phone = request.session.get('phone')
    if request.method == 'POST':
        user_code = request.POST.get('code')
        real_code = cache.get(phone)
        if user_code == real_code:
            request.session['phone_verified'] = True
            print(request.session['phone_verified'])
            return redirect('app_auth:register')
        else:
            messages.error(request, 'Kod noto‘g‘ri!')
    return render(request, 'auth/verify.html')

class RegisterView(View):        
    def get(self, request):
        if request.session.get('phone_verified') != True:
            return redirect('app_auth:phone')
        form = forms.RegisterForm()
        return render(request, 'auth/signup.html', {"form": form})
        
    def post(self, request):
        if request.session.get('phone_verified') != True:
                return redirect('app_auth:phone')
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            password1 = form.cleaned_data['password1']
            try:
                user = User.objects.create_user(
                    username=phone,
                    first_name=first_name,
                    last_name=last_name,
                    password=password1
                )
                # Profil maydonini to‘ldirish (misol uchun)
                user.profile.subscription = day  # 'day' oldindan aniqlangan bo‘lishi kerak
                user.profile.save()
                request.session.pop('phone_verified', None)
                request.session.pop('phone', None)
                return redirect('app_auth:login')
            except Exception as e:
                form.add_error('phone', f"❌ Xatolik: {str(e)}")
        else:
            form.add_error(None, "❌ Formani to'g'ri to'ldiring.")

        return render(request, "auth/signup.html", {"form": form})
    
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
                first_name = profile_form.cleaned_data['first_name']
                last_name = profile_form.cleaned_data['last_name']
                phone = profile_form.cleaned_data['phone']
                username = profile_form.cleaned_data['username']

                user = request.user

                if username:
                    user.username = username
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
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
        