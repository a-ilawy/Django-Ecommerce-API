from django.urls import path
from .views.category import CategoryListCreateView, CategoryDetailView
from .views.brand import BrandListCreateView, BrandDetailView

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<uuid:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("brands/", BrandListCreateView.as_view(), name="brand-list-create"),
    path("brands/<uuid:pk>/", BrandDetailView.as_view(), name="brand-detail"),
]
