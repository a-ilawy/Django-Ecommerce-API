from rest_framework.routers import DefaultRouter
from orders.views.orderView import OrderViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='orders')

urlpatterns = router.urls
