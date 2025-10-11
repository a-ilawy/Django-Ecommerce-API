import random
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from accounts.models.EmailOTP import EmailOTP
from accounts.serializers.password import (
    ForgotPasswordSerializer,
    VerifyResetOTPSerializer,
    ResetPasswordConfirmSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
             return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


        otp_code = str(random.randint(100000, 999999))
        EmailOTP.objects.filter(user=user, is_verified=False).delete() # used for expiration and rate limiting of request otp [later :)]
        EmailOTP.objects.create(user=user, otp=otp_code)

        send_mail(
            'Password Reset Code',
            f'Your password reset OTP is {otp_code}',
            'noreply@shop.com',
            [user.email],
        )
        return Response({'detail': 'If the email exists, an OTP has been sent.'}, status=status.HTTP_200_OK)


class VerifyResetOTPView(APIView):
    def post(self, request):
        serializer = VerifyResetOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        otp_obj = EmailOTP.objects.filter(user=user, otp=otp, is_verified=False).last()
        if not otp_obj:
            return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_obj.created_at < timezone.now() - timedelta(minutes=10):
            return Response({'detail': 'OTP expired.'}, status=status.HTTP_400_BAD_REQUEST)

        otp_obj.is_verified = True
        otp_obj.save()
        return Response({'detail': 'OTP verified.'}, status=status.HTTP_200_OK)


class ResetPasswordConfirmView(APIView):
    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if new_password != confirm_password:
            return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        otp_obj = EmailOTP.objects.filter(user=user, is_verified=True).order_by('-created_at').first()
        if not otp_obj:
            return Response({'detail': 'No verified OTP found.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_obj.created_at < timezone.now() - timedelta(minutes=10):
            return Response({'detail': 'OTP expired.'}, status=status.HTTP_400_BAD_REQUEST)

        # otp_obj.delete()
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password has been reset.'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
