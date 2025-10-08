from rest_framework import serializers
from ..models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "factory",
            "short_description",
            "description",
            "price",
            "category",
            "category_name",
            "brand",
            "brand_name",
            "stock",
            "code",
            "number_of_sales",
            "rating",
            "number_of_ratings",
            "size",
            "color",
            "weight",
            "additional_info",
            "created_at",
            "updated_at",
        ]
