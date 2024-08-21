from django.test import TestCase
from orders.models import Order, OrderItem
from account.factories import UserFactory
from products.factories import ProductVariantFactory

class OrderModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_create_order(self):
        order = Order.objects.create(user=self.user, completed=False)
        self.assertEqual(str(order), f'Order {order.id} by user {self.user}')
        self.assertFalse(order.completed)

    def test_get_total_price(self):
        order = Order.objects.create(user=self.user)
        product1 = ProductVariantFactory(price=100)
        product2 = ProductVariantFactory(price=200)
        OrderItem.objects.create(order=order, product_variant=product1, price=100, quantity=2)
        OrderItem.objects.create(order=order, product_variant=product2, price=200, quantity=1)
        self.assertEqual(order.get_total_price(), 400)

class OrderItemModelTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(user=UserFactory())

    def test_create_order_item(self):
        product = ProductVariantFactory(price=150)
        order_item = OrderItem.objects.create(order=self.order, product_variant=product, price=150, quantity=3)
        self.assertEqual(str(order_item), str(order_item.id))
        self.assertEqual(order_item.get_cost(), 450)
