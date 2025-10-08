from rest_framework import serializers
from ..models.brand import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "image", "created_at", "updated_at"]
