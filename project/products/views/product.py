from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models.product import Product
from ..serializers.product import ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Search & Filter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "brand", "color", "size"]
    search_fields = ["name", "factory", "description"]
    ordering_fields = ["price", "rating", "number_of_sales"]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
