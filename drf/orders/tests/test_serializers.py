from account.factories import AddressFactory, UserFactory
from django.test import TestCase
from products.factories import ProductFactory, ProductVariantFactory
from rest_framework.exceptions import ValidationError

from orders.factories import OrderFactory, OrderItemFactory
from orders.models import Order, OrderItem
from orders.serializers import (
    OrderAdminSerializer,
    OrderItemSerializer,
    OrderSerializer,
)


class OrderItemSerializerTest(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.product_variant = ProductVariantFactory(product=self.product)
        self.order_item = OrderItemFactory(product_variant=self.product_variant)
        self.serializer = OrderItemSerializer(instance=self.order_item)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ["id", "product_variant", "product_name", "price", "quantity", "added_at"],
        )

    def test_product_name_field_content(self):
        self.assertEqual(self.serializer.data["product_name"], self.product.title)

    def test_added_at_format(self):
        self.assertRegex(
            self.serializer.data["added_at"],
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{4}$",
        )

    def test_validate_quantity(self):
        serializer = OrderItemSerializer()
        self.assertEqual(serializer.validate_quantity(1), 1)
        self.assertEqual(serializer.validate_quantity(5), 5)
        with self.assertRaises(ValidationError):
            serializer.validate_quantity(0)
        with self.assertRaises(ValidationError):
            serializer.validate_quantity(-1)


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.address = AddressFactory(user=self.user)
        self.order = OrderFactory(
            user=self.user, shipping_address=self.address, items__have_items=False
        )
        self.order_item = OrderItemFactory(order=self.order)
        self.serializer = OrderSerializer(instance=self.order)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "id",
                "user",
                "items",
                "total_price",
                "status",
                "created_at",
                "updated_at",
            ],
        )

    def test_user_field_content(self):
        self.assertEqual(self.serializer.data["user"], self.user.id)

    def test_total_price_calculation(self):
        self.assertEqual(
            self.serializer.data["total_price"], self.order_item.get_cost()
        )

    def test_created_at_format(self):
        self.assertRegex(
            self.serializer.data["created_at"],
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{4}$",
        )

    def test_updated_at_format(self):
        self.assertRegex(
            self.serializer.data["updated_at"],
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{4}$",
        )

    def test_create_order(self):
        product_variant = ProductVariantFactory()
        data = {
            "user": self.user.id,
            "shipping_address": self.address.id,
            "items": [
                {
                    "product_variant": product_variant.id,
                    "quantity": 2,
                    "price": product_variant.price,
                }
            ],
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(OrderItem.objects.filter(order=order).count(), 1)


class OrderAdminSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.address = AddressFactory(user=self.user)
        self.order = OrderFactory(user=self.user, shipping_address=self.address)
        self.order_item = OrderItemFactory(order=self.order)
        self.serializer = OrderAdminSerializer(instance=self.order)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "id",
                "user",
                "user_email",
                "items",
                "total_price",
                "status",
                "created_at",
                "updated_at",
            ],
        )

    def test_user_email_field_content(self):
        self.assertEqual(self.serializer.data["user_email"], self.user.email)
