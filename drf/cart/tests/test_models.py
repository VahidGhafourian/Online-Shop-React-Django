from django.test import TestCase
from cart.models import Cart, CartItem
from account.models import User
from products.models import ProductVariant
from cart.factories import CartFactory, CartItemFactory
from account.factories import UserFactory
from products.factories import ProductVariantFactory

class CartModelTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.cart = CartFactory(user=self.user)

    def test_cart_creation(self):
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(self.cart.user, self.user)

    def test_cart_str_representation(self):
        self.assertEqual(str(self.cart), f"{self.cart.id}")


class CartItemModelTest(TestCase):

    def setUp(self):
        self.cart = CartFactory()
        self.product_variant = ProductVariantFactory()
        self.cart_item = CartItemFactory(cart=self.cart, product_variant=self.product_variant)

    def test_cart_item_creation(self):
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product_variant, self.product_variant)

    def test_cart_item_str_representation(self):
        self.assertEqual(str(self.cart_item), f"{self.cart_item.id} in cart {self.cart.id}")
