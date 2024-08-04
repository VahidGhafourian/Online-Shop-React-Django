import factory
from factory.django import DjangoModelFactory
from .models import Order, OrderItem
from account.factory import UserFactory
from products.factory import ProductFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    completed_at = factory.Faker('boolean')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')

# OrderItemFactory
class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    price = factory.Faker('random_number', digits=5)
    quantity = factory.Faker('random_int', min=1, max=10)
    added_at = factory.Faker('date_time_this_year')
