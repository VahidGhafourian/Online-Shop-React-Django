import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Cart, CartItem
from account.factory import UserFactory
from products.factory import ProductVariantFactory

class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product_variant = factory.SubFactory(ProductVariantFactory)
    items_count = factory.Faker('random_int', min=1, max=10)
    added_at = factory.Faker('date_time_this_year')
