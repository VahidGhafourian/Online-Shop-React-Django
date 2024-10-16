from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from orders.factories import (
    AddressFactory,
    OrderFactory,
    OrderItemFactory,
    ProductVariantFactory,
    UserFactory,
)
from orders.models import Order, OrderItem


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.address = AddressFactory(user=self.user)
        self.order = OrderFactory(
            user=self.user,
            shipping_address=self.address,
            status=Order.Status.PENDING,
            items__have_items=False,
        )

    def test_order_creation(self):
        self.assertTrue(isinstance(self.order, Order))
        self.assertEqual(
            self.order.__str__(),
            f"Order {self.order.id} by user {str(self.order.user)}",
        )

    def test_order_status(self):
        self.assertEqual(self.order.status, Order.Status.PENDING)
        self.order.status = Order.Status.PAID
        self.order.save()
        self.assertEqual(self.order.status, Order.Status.PAID)

    def test_order_dates(self):
        self.assertTrue(isinstance(self.order.created_at, timezone.datetime))
        self.assertTrue(isinstance(self.order.updated_at, timezone.datetime))

    def test_get_total_price(self):
        item1 = OrderItemFactory(order=self.order, price=10000, quantity=2)
        item2 = OrderItemFactory(order=self.order, price=5000, quantity=1)
        self.assertEqual(self.order.get_total_price(), 25000)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.order = OrderFactory()
        self.product_variant = ProductVariantFactory()
        self.order_item = OrderItemFactory(
            order=self.order,
            product_variant=self.product_variant,
            price=1000,
            quantity=2,
        )

    def test_order_item_creation(self):
        self.assertTrue(isinstance(self.order_item, OrderItem))
        self.assertEqual(self.order_item.__str__(), str(self.order_item.id))

    def test_get_cost(self):
        self.assertEqual(self.order_item.get_cost(), 2000)

    def test_negative_price(self):
        with self.assertRaises(ValidationError):
            OrderItemFactory(
                order=self.order, product_variant=self.product_variant, price=-100
            )

    def test_zero_quantity(self):
        with self.assertRaises(ValidationError):
            OrderItemFactory(
                order=self.order, product_variant=self.product_variant, quantity=0
            )

    def test_order_item_added_at(self):
        self.assertTrue(isinstance(self.order_item.added_at, timezone.datetime))
