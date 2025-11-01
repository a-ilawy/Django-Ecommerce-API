from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from orders.models.order import Order
from orders.serializers.OrderSerializer import OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if not user or not user.is_authenticated:
            return Order.objects.none()
       
        if user.is_staff or user.user_type == "admin":
            return Order.objects.all().select_related("user").prefetch_related("items__product")
       
        return Order.objects.filter(user=user).select_related("user").prefetch_related("items__product")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_order(self, request, pk=None):
        try:
            order = self.get_object()
        except Http404:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.user != request.user and request.user.user_type !='admin':
            return Response({"error": "You are not allowed to cancel this order."}, status=status.HTTP_403_FORBIDDEN)


        if order.status not in ["pending", "processing"]:
            return Response(
                {"error": f"Cannot cancel order in '{order.status}' status"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

        order.status = "cancelled"
        order.save()

        return Response(
            {"message": "Order cancelled successfully and products restocked."},
            status=status.HTTP_200_OK,
        )
