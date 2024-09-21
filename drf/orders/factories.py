import factory
from faker import Faker
from factory.django import DjangoModelFactory
from .models import Order, OrderItem
from account.factories import UserFactory
from products.factories import ProductVariantFactory
from django.utils import timezone
from account.factories import AddressFactory

fake = Faker()

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    transaction_id = factory.LazyFunction(lambda: fake.unique.uuid4())
    status = factory.Iterator([choice[0] for choice in Order.Status.choices])
    shipping_address = factory.SubFactory(AddressFactory)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for item in extracted:
                self.items.add(item)
        else:
            # Create 1 to 5 OrderItems by default
            OrderItemFactory.create_batch(fake.random_int(min=1, max=5), order=self)

class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product_variant = factory.SubFactory(ProductVariantFactory)
    price = factory.Faker('random_int', min=1000, max=100000)
    quantity = factory.Faker('random_int', min=1, max=10)
    added_at = factory.LazyFunction(timezone.now)
