from rest_framework import serializers
from orders.models.order import Order, OrderItem
from products.models.product import Product
from orders.serializers.OrderItemSerializer import OrderItemSerializer
from rest_framework.exceptions import ValidationError

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'status',
            'total_price',
            'shipping_address',
            'phone_number',
            'items',
            'created_at',
        ]
        read_only_fields = ['user', 'total_price', 'status', 'created_at']

    def create(self, validated_data):

        order = Order.objects.create(**validated_data)
        items_data = self.initial_data.get('items', [])
        if not items_data:
            raise ValidationError("Order must contain at least one item.")
        
        total = 0
        for item in items_data:
            product = item['product']
            quantity = item.get('quantity', 1)
            if not Product.objects.filter(id=product).exists():
                raise ValidationError(f"Product with id {product} does not exist.")
            product = Product.objects.get(id=item['product'])

            if product.stock < quantity:
                res = {
                    "product id": product.id,
                    "product name": product.name,
                    "stock": product.stock,
                    "order quantity":quantity,
                    "message": "out of stock"
                }
                raise ValidationError(res)
            
            price = product.price
            
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
            )
            product.stock -= quantity
            product.save()
            total += order_item.subtotal or (price * quantity)

        order.total_price = total
        order.save()

        return order
