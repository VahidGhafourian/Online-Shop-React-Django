from django.test import TestCase
from cart.serializers import CartSerializer, CartItemSerializer
from cart.factories import CartFactory, CartItemFactory
from products.factories import ProductVariantFactory

class CartSerializerTest(TestCase):

    def setUp(self):
        self.cart = CartFactory()
        self.cart_item = CartItemFactory(cart=self.cart)

    def test_cart_serializer(self):
        serializer = CartSerializer(self.cart)
        self.assertEqual(serializer.data['id'], self.cart.id)
        self.assertEqual(len(serializer.data['items']), 1)

    def test_cart_item_serializer(self):
        serializer = CartItemSerializer(self.cart_item)
        self.assertEqual(serializer.data['id'], self.cart_item.id)
        self.assertEqual(serializer.data['items_count'], self.cart_item.items_count)
