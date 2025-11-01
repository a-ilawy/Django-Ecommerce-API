import pytest
from rest_framework import status
from accounts.tests.factories.user_factory import UserFactory
from .factories.order_factory import AdminFactory


@pytest.mark.django_db
def test_cancel_order_success(api_client, order_with_items, cancel_url):
    user = order_with_items.user
    product = order_with_items.items.first().product
    old_stock = product.stock

    api_client.force_authenticate(user=user)
    response = api_client.post(cancel_url)

    assert response.status_code == status.HTTP_200_OK
    order_with_items.refresh_from_db()
    product.refresh_from_db()
    assert order_with_items.status == "cancelled"
    assert product.stock == old_stock + 2


@pytest.mark.django_db
def test_admin_can_cancel_any_order(api_client, order_with_items, cancel_url):
    admin = AdminFactory()
    product = order_with_items.items.first().product
    old_stock = product.stock

    api_client.force_authenticate(user=admin)
    response = api_client.post(cancel_url)

    assert response.status_code == status.HTTP_200_OK
    order_with_items.refresh_from_db()
    product.refresh_from_db()
    assert order_with_items.status == "cancelled"
    assert product.stock == old_stock + 2


@pytest.mark.django_db
def test_user_cannot_cancel_other_user_order(api_client, order_with_items, cancel_url):
    other_user = UserFactory()
    api_client.force_authenticate(user=other_user)

    response = api_client.post(cancel_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.data["error"].lower()


@pytest.mark.django_db
def test_cannot_cancel_non_pending_order(api_client, order_with_items, cancel_url):
    order_with_items.status = "shipped"
    order_with_items.save()

    api_client.force_authenticate(user=order_with_items.user)
    response = api_client.post(cancel_url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "cannot cancel" in response.data["error"].lower()
