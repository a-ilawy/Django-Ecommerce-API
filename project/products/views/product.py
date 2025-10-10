from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models.product import Product
from ..serializers.product import ProductSerializer
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('created_at')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    # Search & Filter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "brand", "color", "size"]
    search_fields = ["name", "factory", "description"]
    ordering_fields = ["price", "rating", "number_of_sales"]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
