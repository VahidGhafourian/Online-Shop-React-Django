import factory
from factory.django import DjangoModelFactory
from .models import Order, OrderItem
from account.factories import UserFactory
from products.factories import ProductVariantFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    completed_at = factory.Faker('boolean')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')

class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product_variant = factory.SubFactory(ProductVariantFactory)
    price = factory.Faker('random_number', digits=5)
    quantity = factory.Faker('random_int', min=1, max=10)
    added_at = factory.Faker('date_time_this_year')
