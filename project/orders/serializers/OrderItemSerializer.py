from rest_framework import serializers
from orders.models.order import OrderItem
from products.models.product import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'order',
            'product',
            'product_name',
            'quantity',
            'price',
            'subtotal',
        ]
        read_only_fields = ['subtotal']
