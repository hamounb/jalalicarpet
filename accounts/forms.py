from django import forms
from django.core.exceptions import ValidationError
from .models import AddressModel
from django.contrib.auth.models import User


def is_mobile(value):
    if not str(value).isnumeric() or len(value) !=11 or str(value)[0] != '0':
        raise ValidationError('شماره موبایل صحیح نمی‌باشد!')
    
def is_number(value):
    if not str(value).isnumeric():
        raise ValidationError('لطفا فقط عدد وارد نمایید!')
    
def is_postal(value):
    if len(value) != 10 or not str(value).isnumeric():
        raise ValidationError('کد پستی صحیح نمی‌باشد!')


class SignUpForm(forms.Form):
    first_name = forms.CharField(label="نام", required=True, max_length=100, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"نام"}))
    last_name = forms.CharField(label="نام خانوادگی", required=True, max_length=100, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"نام خانوادگی"}))
    mobile = forms.CharField(label="شماره موبایل", required=True, max_length=11, validators=[is_mobile], widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"شماره موبایل"}))
    password = forms.CharField(label="رمز عبور", required=True, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"رمز عبور"}))
    password1 = forms.CharField(label="تکرار رمز عبور", required=True, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"تکرار رمز عبور"}))


class SignInForm(forms.Form):
    username = forms.CharField(max_length=11, validators=[is_mobile], label="شماره موبایل",  widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"شماره موبایل"}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"رمز عبور"}))


class TokenForm(forms.Form):
    code = forms.CharField(max_length=6, required=True, validators=[is_number],  widget=forms.TextInput(attrs={"class":"text-center form-control rounded"}))