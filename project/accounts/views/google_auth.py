import requests
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class GoogleLoginView(APIView):


    def post(self, request):
        access_token = request.data.get("access_token")

        if not access_token:
            return Response(
                {"detail": "access_token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        google_response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if google_response.status_code != 200:
            return Response(
                {"detail": "Invalid Google token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_info = google_response.json()
        email = user_info.get("email")
        name = user_info.get("name")
        picture = user_info.get("picture")
        email_verified = user_info.get("email_verified", False)

        if not email or not email_verified:
            return Response(
                {"detail": "Email not verified by Google"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "is_active": True,
                "user_type": "buyer",
            },
        )

        if created:
            if hasattr(user, "full_name"):
                user.full_name = name
                user.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                # "detail": "Login successful" if not created else "User registered successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_type": user.user_type,
            },
            status=status.HTTP_200_OK,
        )
