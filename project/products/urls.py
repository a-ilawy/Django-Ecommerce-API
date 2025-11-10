from django.urls import path
from .views.category import CategoryListCreateView, CategoryDetailView
from .views.brand import BrandListCreateView, BrandDetailView
from .views.product import ProductListCreateView, ProductDetailView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', ProductListCreateView, basename='product')

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<uuid:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("brands/", BrandListCreateView.as_view(), name="brand-list-create"),
    path("brands/<uuid:pk>/", BrandDetailView.as_view(), name="brand-detail"),
    # path("", ProductListCreateView.as_view(), name="product-list-create"),
    path("<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
]

urlpatterns += router.urls
