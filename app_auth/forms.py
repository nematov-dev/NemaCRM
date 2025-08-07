from typing import Any
from django import forms
from django.contrib import messages

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    phone = forms.CharField(max_length=50)
    password1 = forms.CharField()
    password2 = forms.CharField()

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("password1")
        pass2 = cleaned_data.get("password2")

        if pass1 != pass2:
            self.add_error(None, "Parol va tasdiqlash paroli bir xil emas!")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput,max_length=128)

class ProfileForm(forms.Form):
    image = forms.FileField(required=False)
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    phone = forms.CharField(max_length=30,required=False)
    username = forms.CharField(max_length=128)

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("new_password1")
        pass2 = cleaned_data.get("new_password2")

        if pass1 != pass2:
            self.add_error(None, "Yangi parol va tasdiqlash paroli bir xil emas!")
        return cleaned_data