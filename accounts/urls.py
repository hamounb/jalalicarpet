from django.urls import path

from .views import *

app_name="accounts"

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("mobile-verify/<str:mobile>/", MobileVerifyView.as_view(), name="mobile-verify"),
    path("token-send/<str:mobile>/", TokenSendView.as_view(), name="token-send"),
]