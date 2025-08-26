from datetime import date,timedelta,datetime
import random

from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from django.utils import timezone

from app_auth import forms
from app_auth.utils import send_verification_code

User = get_user_model()

today_date = date.today()
day = today_date + timedelta(days=30)

# date → datetime qilib olish
day_datetime = datetime.combine(day, datetime.min.time())

# timezone qo‘shib berish
day_datetime = timezone.make_aware(day_datetime)

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
                    form.add_error(None, "Email yoki parol notug'ri!")
            else:
                form.add_error(None, "Email raqam yoki parol notug'ri!")
        else:
            form.add_error(None, "Formani to‘ldiring!")
        return render(request, 'auth/signin.html', {'form': form})
    
def phone_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if not User.objects.filter(username=phone).exists():
            code = str(send_verification_code(phone))
            cache.set(f"verify:{phone}", code, 300)  # 5 daqiqa
            request.session['phone'] = phone
            return redirect('app_auth:verify')
        else:
            messages.error(request,"Bu email bilan foydalanuvchi allaqachon mavjud.")
    return render(request, 'auth/phone.html')

def verify_view(request):
    phone = request.session.get('phone')
    if request.method == 'POST':
        user_code = request.POST.get('code')
        real_code = cache.get(f"verify:{phone}")
        print(real_code)
        if str(user_code) == str(real_code):
            request.session['phone_verified'] = True
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
                user.profile.subscription = day_datetime  # 'day' oldindan aniqlangan bo‘lishi kerak
                user.profile.save()
                request.session.pop('phone_verified', None)
                request.session.pop('phone', None)
                messages.success(request,"Ro'yxatdan o'tingiz tizimga kirishigiz mumkin!")
                return redirect('app_auth:register')
            
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
        
class ForgetPasswordView(View):
    def get(self,request):
        return render(request,"auth/password-forget.html")
    
    def post(self,request):
        password_phone = request.POST.get('password_phone')
        if User.objects.filter(username=password_phone).exists():
            code = send_verification_code(password_phone)
            cache.set(f"verify:{password_phone}", code, 300)  # 5 daqiqa
            request.session['password_phone'] = password_phone
            return redirect('app_auth:password-forget-confirm')
        else:
            messages.error(request,"Bu email bilan foydalanuvchi mavjud emas.")
        return render(request,"auth/password-forget.html")
    
class ForgetPasswordConfimView(View):
    def get(self,request):
        return render(request,'auth/password-forget-confirm.html')

    def post(self,request):
        password_phone = request.session.get('password_phone')
        user_code = request.POST.get('password_code')
        real_code = cache.get(f"verify:{password_phone}")
        if user_code == real_code:
            request.session['password_phone_verified'] = True
            return redirect('app_auth:password-forget-done')
        else:
            messages.error(request, 'Kod noto‘g‘ri!')
        return render(request,'auth/password-forget-confirm.html')

class ForgetPasswordDone(View):
    def get(self,request):
        if request.session.get('password_phone_verified') != True:
            return redirect('app_auth:password-forget')
        return render(request,'auth/password-forget-done.html')
    
    def post(self,request):
        if request.session.get('password_phone_verified') != True:
            return redirect('app_auth:password-forget')
        form = forms.ForgetPasswordForm(request.POST)
        if form.is_valid():
            password_phone = request.session.get('password_phone')
            new_password = form.cleaned_data['new_password1']
            try:
                user = User.objects.get(username=password_phone)
                user.set_password(new_password)
                user.save()
                messages.success(request,"Parolingiz o'zgartirildi!")
                request.session.pop('password_phone_verified', None)
                request.session.pop('password_phone', None)
                
            except Exception as e:
                    form.add_error(None, f"❌ Xatolik: {str(e)}")
        else:
            messages.error(request,"Yangi parol va tasdiqlash paroli bir xil emas!")

        return render(request,'auth/password-forget-done.html')


                


        