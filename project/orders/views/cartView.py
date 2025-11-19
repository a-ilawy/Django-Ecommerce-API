from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models.cart import Cart, CartItem
from products.models import Product
from ..serializers.cartSerializer import CartSerializer
from ..serializers.OrderSerializer import OrderSerializer

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @action(detail=False, methods=['get'], url_path='view')
    def view_cart(self, request):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='add')
    def add_to_cart(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart = self.get_cart(request.user)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        if item.quantity > product.stock:
            return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)

        item.save()

        return Response({"message": f"{product.name} added to cart"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='update')
    def update_item(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        cart = self.get_cart(request.user)
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        return Response({"message": "Cart updated successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='remove')
    def remove_item(self, request, pk=None):
        cart = self.get_cart(request.user)
        item = get_object_or_404(CartItem, cart=cart, pk=pk)
        item.delete()

        return Response({"message": "Item removed"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request):

        cart = self.get_cart(request.user)

        if not cart.items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        shipping_address = request.data.get("shipping_address")
        phone_number = request.data.get("phone_number")

        if not shipping_address or not phone_number:
            return Response(
                {"error": "Shipping address and phone number are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "user": request.user.id,
            "shipping_address": shipping_address,
            "phone_number": phone_number,
            "items": [
                {
                    "product": item.product.id,
                    "quantity": item.quantity
                }
                for item in cart.items.all()
            ]
        }

        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)

        cart.items.all().delete()

        return Response(
            {
                "message": "Checkout successful",
                "order": OrderSerializer(order).data
            },
            status=status.HTTP_201_CREATED
        )