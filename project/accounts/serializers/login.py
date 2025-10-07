from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # add custom fields
        data['user_type'] = user.user_type
        if user.user_type == "admin" and hasattr(user, "admin_profile"):
            data['role'] = user.admin_profile.role
        
        return data