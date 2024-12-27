from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django import views
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .melipayamak import send_token

# Create your views here.

class SignUpView(views.View):

    def get(self, request):
        form = SignUpForm()
        return render(request, "accounts/sign-up.html", {"form":form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            mobile = form.cleaned_data.get("mobile")
            password = form.cleaned_data.get("password")
            password1 = form.cleaned_data.get("password1")
            try:
                user = User.objects.get(username=mobile)
            except User.DoesNotExist:
                if password and password1 and password == password1:
                    new_user = User()
                    new_user.first_name = first_name
                    new_user.last_name = last_name
                    new_user.username = mobile
                    new_user.set_password(password)
                    new_user.is_active = False
                    new_user.save()
                    send = send_token(number=mobile)
                    if send is not None:
                        token = TokenModel(
                            user = new_user,
                            user_created = new_user,
                            user_modified = new_user,
                            token = send["code"],
                            status = send["status"],
                            recid = send["recid"]
                        )
                        token.save()
                        messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                        return redirect("accounts:mobile-verify", mobile=new_user.username)
                    return
                messages.error(request, "رمز عبور و تکرار رمز عبور باید مشابه باشد!")
                return render(request, "accounts/sign-up.html", {"form":form})
            else:
                if user.is_active:
                    messages.error(request, "با این شماره همراه حساب کاربری ایجاد کرده‌اید، لظفا وارد حساب کاربری شوید.")
                    return render(request, "accounts/sign-up.html", {"form":form})
                if password and password1 and password == password1:
                    user.set_password(password)
                    user.save()
                    try:
                        token = TokenModel.objects.get(user=user)
                    except TokenModel.DoesNotExist:
                        send = send_token(number=user.username)
                        if send is not None:
                            token = TokenModel(
                                user = user,
                                user_created = user,
                                user_modified = user,
                                token = send["code"],
                                status = send["status"],
                                recid = send["recid"]
                            )
                            token.save()
                            messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                            return redirect("accounts:mobile-verify", mobile=user.username)
                        return
                    else:
                        send = send_token(number=user.username)
                        if send is not None:
                            token.token = send["code"]
                            token.status = send["status"]
                            token.recid = send["recid"]
                            token.save()
                            messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                            return redirect("accounts:mobile-verify", mobile=user.username)
                        return
                messages.error(request, "رمز عبور و تکرار رمز عبور باید مشابه باشد!")
                return render(request, "accounts/sign-up.html", {"form":form})
        return render(request, "accounts/sign-up.html", {"form":form})
    

class MobileVerifyView(views.View):

    def get(self, request, mobile):
        user = get_object_or_404(User, username=mobile)
        if user.is_active:
            return redirect("accounts:profile")
        form = TokenForm()
        context = {
            "form":form,
            "mobile":mobile
            }
        return render(request, "accounts/mobile-verify.html", context)
    
    def post(self, request, mobile):
        user = get_object_or_404(User, username=mobile)
        if user.is_active:
            return redirect("accounts:profile")
        try:
            token = TokenModel.objects.get(user=user)
        except TokenModel.DoesNotExist:
            return redirect("accounts:sign-up")
        form = TokenForm(request.POST)
        context = {
            "form":form,
            "mobile":mobile,
        }
        if form.is_valid():
            code = form.cleaned_data.get("code")
            if token.token == code:
                user.is_active = True
                user.save()
                login(request, user)
                return redirect("accounts:profile")
            messages.error(request, "رمز یکبارمصرف اشتباه است!")
            return render(request, "accounts/mobile-verify.html", context)
        return render(request, "accounts/mobile-verify.html", context)
    

class TokenSendView(views.View):

    def get(self, request, mobile):
        user = get_object_or_404(User, username=mobile)
        if user.is_active:
            return redirect("")
        try:
            token = TokenModel.objects.get(user__username=mobile)
        except TokenModel.DoesNotExist:
            send = send_token(number=user.username)
            if send is not None:
                token = TokenModel(
                    user = user,
                    user_created = user,
                    user_modified = user,
                    token = send["code"],
                    status = send["status"],
                    recid = send["recid"]
                )
                token.save()
                messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                return redirect("accounts:mobile-verify", mobile=user.username)
            return
        else:
            send = send_token(number=user.username)
            if send is not None:
                token.token = send["code"]
                token.status = send["status"]
                token.recid = send["recid"]
                token.save()
                messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                return redirect("accounts:mobile-verify", mobile=user.username)
            return
