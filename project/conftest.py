import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.tests.factories.user_factory import UserFactory
from orders.tests.factories.order_factory import OrderFactory, OrderItemFactory, ProductFactory


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_factory():
    return UserFactory

@pytest.fixture
def order_with_items(db):
    product = ProductFactory(stock=10, price=100)
    order = OrderFactory()
    OrderItemFactory(order=order, product=product, quantity=2, price=product.price)
    return order


@pytest.fixture
def cancel_url(order_with_items):
    return reverse("orders-cancel-order", args=[order_with_items.pk])
