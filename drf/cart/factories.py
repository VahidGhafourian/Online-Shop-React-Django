import factory
from account.factories import UserFactory
from django.utils import timezone
from factory.django import DjangoModelFactory
from faker import Faker
from products.factories import ProductVariantFactory

from .models import Cart, CartItem

fake = Faker()


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    status = factory.Iterator([choice[0] for choice in Cart.Status.choices])
    coupon = None  # factory.SubFactory(CouponFactory)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for item in extracted:
                self.items.add(item)
        else:
            # Create 1 to 5 OrderItems by default
            CartItemFactory.create_batch(fake.random_int(min=1, max=5), cart=self)


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product_variant = factory.SubFactory(ProductVariantFactory)
    quantity = factory.Faker("random_int", min=1, max=3)
    price = factory.Faker(
        "random_int", min=1000, max=100000
    )  # Assuming price is in cents
    added_at = factory.LazyFunction(timezone.now)
