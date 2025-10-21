from django.urls import path
from accounts.views.login import CustomLoginView
from accounts.views.verifyOTP import VerifyOTPView
from accounts.views.register import RegisterView
from accounts.views.passwords import (
    ForgotPasswordView,
    VerifyResetOTPView,
    ResetPasswordConfirmView,
    ChangePasswordView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views.logout import LogoutView
from accounts.views.google_auth import GoogleLoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/", VerifyOTPView.as_view(), name="verify-otp"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/forgot/", ForgotPasswordView.as_view(), name="password-forgot"),
    path("password/verify-otp/", VerifyResetOTPView.as_view(), name="password-verify-otp"),
    path("password/reset/confirm/", ResetPasswordConfirmView.as_view(), name="password-reset-confirm"),
    path("password/change/", ChangePasswordView.as_view(), name="password-change"),
    path("google-login/", GoogleLoginView.as_view(), name="google-login"),
]
