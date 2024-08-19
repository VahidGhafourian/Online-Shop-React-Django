from django.test import TestCase
from orders.serializers import OrderSerializer, OrderItemSerializer
from orders.models import Order, OrderItem
from account.factories import UserFactory
from products.factories import ProductVariantFactory
from products.serializers import ProductVariantSerializer

class OrderSerializerTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_order_serialization(self):
        order = Order.objects.create(user=self.user, completed_at=False)
        serializer = OrderSerializer(order)
        expected_data = {
            'id': order.id,
            'user': self.user.id,
            'completed_at': False,
            'total_price': 0,
            'items': [],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_order_validation(self):
        serializer = OrderSerializer(data={'completed_at': False})
        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)

class OrderItemSerializerTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(user=UserFactory())

    def test_order_item_serialization(self):
        product_variant = ProductVariantFactory()
        order_item = OrderItem.objects.create(order=self.order, product_variant=product_variant, price=100, quantity=2)
        serializer = OrderItemSerializer(order_item)

        product_variant_serialized = ProductVariantSerializer(product_variant).data

        expected_data = {
            'id': order_item.id,
            'order': self.order.id,
            'product_variant': product_variant_serialized,
            'price': 100,
            'quantity': 2,
        }

        self.assertEqual(serializer.data, expected_data)

    def test_order_item_validation(self):
        serializer = OrderItemSerializer(data={'price': -100, 'quantity': 0, 'order': self.order})
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
        self.assertIn('quantity', serializer.errors)
