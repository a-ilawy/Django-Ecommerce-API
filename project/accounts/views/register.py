from rest_framework import generics
from accounts.serializers.register import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer