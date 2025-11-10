import factory
from faker import Faker
from orders.models.order import Order, OrderItem
from accounts.tests.factories.user_factory import UserFactory
from products.tests.factories.products_factory import ProductFactory

fake = Faker()


class AdminFactory(UserFactory):
    user_type = "admin"
    is_staff = True


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    status = "pending"
    shipping_address = factory.LazyAttribute(lambda _: fake.address())
    phone_number = factory.LazyAttribute(lambda _: fake.phone_number())
    total_price = 0


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=3))
    price = factory.SelfAttribute("product.price")
