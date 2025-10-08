from rest_framework import serializers
from ..models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image", "created_at", "updated_at"]
