from rest_framework.routers import DefaultRouter
from orders.views.orderView import OrderViewSet
from .views.cartView import CartViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='orders')

router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = router.urls
