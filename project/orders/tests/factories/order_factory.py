import factory
from faker import Faker
from django.contrib.auth import get_user_model
from products.models.product import Product
from orders.models.order import Order, OrderItem
from accounts.tests.factories.user_factory import UserFactory
from products.models.category import Category
from products.models.brand import Brand

fake = Faker()


class AdminFactory(UserFactory):
    user_type = "admin"
    is_staff = True



class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: fake.word())


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.LazyAttribute(lambda _: fake.word())
    
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda _: fake.word())
    price = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=3, right_digits=2, positive=True))
    stock = factory.LazyAttribute(lambda _: fake.random_int(min=5, max=20))
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)


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
