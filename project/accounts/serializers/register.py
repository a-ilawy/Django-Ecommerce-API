from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
import random
from accounts.models import EmailOTP


User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data, is_active=False)
        user.set_password(password)
        user.save()

        # Generate OTP
        otp_code = str(random.randint(100000, 999999))
        EmailOTP.objects.create(user=user, otp=otp_code)

        # Send OTP via email
        send_mail(
            "Your Verification Code",
            f"Your OTP code is {otp_code}",
            "noreply@shop.com",
            [user.email],
        )
        return user