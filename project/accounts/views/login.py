from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers.login import CustomTokenObtainPairSerializer

class CustomLoginView(APIView):
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
