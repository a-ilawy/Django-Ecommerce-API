from rest_framework import generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..filters.product_filter import ProductFilter
from django.db.models import Sum
from ..permissions import CustomtPermission
from ..models.product import Product
from ..serializers.product import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class ProductListCreateView(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('created_at')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [CustomtPermission]

    # Search & Filter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "factory", "description"]
    ordering_fields = ["price", "rating", "number_of_sales"]

    @action(detail=False, methods=['get'], url_path='top-selling')
    def get_top_selling(self, request):
        top_products = Product.objects.annotate(
            total_sales=Sum("orderitem__quantity")
        ).order_by("-total_sales")
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomtPermission]
