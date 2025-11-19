from django_filters import rest_framework as filters
from django.db.models import Sum
from ..models.product import Product


class ProductFilter(filters.FilterSet):
    best_seller = filters.BooleanFilter(method='best_seller')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'color', 'size']

    def best_seller(self, queryset, name, value):
        if value:
            queryset = queryset.annotate(total_salse = Sum('orderitem__quantity')).order_by('-total_sales')

            queryset = queryset.filter(total_sales__gte=1)

        return queryset