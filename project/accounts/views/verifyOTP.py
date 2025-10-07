from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accounts.models.user import User
from accounts.models.EmailOTP import EmailOTP

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("otp")
        try:
            user = User.objects.get(email=email)
            otp = EmailOTP.objects.filter(user=user, otp=code, is_verified=False).last()
            if otp:
                otp.is_verified = True
                otp.save()
                user.is_active = True
                user.save()
                return Response({"detail": "Account verified successfully"}, status=200)
            return Response({"detail": "Invalid OTP"}, status=400)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)
