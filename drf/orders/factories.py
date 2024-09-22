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

        have_items = kwargs.pop('have_items', True)
        size = kwargs.pop('size', None)
        if have_items:
            if extracted:
                for item in extracted:
                    self.items.add(item)
            else:
                num_items = size if size is not None else fake.random_int(min=1, max=5)
                OrderItemFactory.create_batch(num_items, order=self)

class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory, items__have_items=False)
    product_variant = factory.SubFactory(ProductVariantFactory)
    price = factory.Faker('random_int', min=1000, max=100000)
    quantity = factory.Faker('random_int', min=1, max=10)
    added_at = factory.LazyFunction(timezone.now)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        obj.full_clean()
        obj.save()
        return obj
