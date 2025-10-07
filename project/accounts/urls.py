from django.urls import path
from accounts.views.login import CustomLoginView
from accounts.views.verifyOTP import VerifyOTPView
from accounts.views.register import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views.logout import LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/", VerifyOTPView.as_view(), name="verify-otp"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
