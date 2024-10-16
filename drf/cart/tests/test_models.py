from account.factories import UserFactory
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from payments.factories import CouponFactory
from products.factories import ProductVariantFactory

from cart.factories import CartItemFactory
from cart.models import Cart, CartItem


class CartModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        self.assertIsInstance(self.cart, Cart)
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(self.cart.status, Cart.Status.ACTIVE)
        self.assertIsNone(self.cart.coupon)

    def test_cart_string_representation(self):
        self.assertEqual(str(self.cart), f"{self.cart.id}")

    def test_cart_total_price(self):
        # Create some cart items
        CartItemFactory(cart=self.cart, quantity=2, price=1000)
        CartItemFactory(cart=self.cart, quantity=1, price=1500)

        expected_total = (2 * 1000) + (1 * 1500)
        self.assertEqual(self.cart.total_price, expected_total)

    def test_cart_status_choices(self):
        self.cart.status = Cart.Status.ABANDONED
        self.cart.save()
        self.assertEqual(self.cart.status, Cart.Status.ABANDONED)

        self.cart.status = Cart.Status.CONVERTED
        self.cart.save()
        self.assertEqual(self.cart.status, Cart.Status.CONVERTED)

    def test_cart_with_coupon(self):
        coupon = CouponFactory()
        self.cart.coupon = coupon
        self.cart.save()
        self.assertEqual(self.cart.coupon, coupon)


class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.cart = Cart.objects.create(user=self.user)
        self.product_variant = ProductVariantFactory()
        self.cart_item = CartItemFactory(
            cart=self.cart, product_variant=self.product_variant
        )

    def test_cart_item_creation(self):
        self.assertIsInstance(self.cart_item, CartItem)
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product_variant, self.product_variant)
        self.assertGreater(self.cart_item.quantity, 0)
        self.assertGreater(self.cart_item.price, 0)

    def test_cart_item_string_representation(self):
        expected_str = f"{self.product_variant.title} in cart {self.cart.id}"
        self.assertEqual(str(self.cart_item), expected_str)

    def test_cart_item_subtotal(self):
        expected_subtotal = self.cart_item.quantity * self.cart_item.price
        self.assertEqual(self.cart_item.subtotal, expected_subtotal)

    def test_cart_item_unique_constraint(self):
        with self.assertRaises(ValidationError):
            CartItemFactory(cart=self.cart, product_variant=self.product_variant)

    def test_cart_item_quantity_validation(self):
        self.cart_item.product_variant.inventory.quantity = 5
        self.cart_item.product_variant.inventory.save()

        self.cart_item.quantity = 6
        with self.assertRaises(ValidationError):
            self.cart_item.save()

    def test_cart_item_product_availability_validation(self):
        self.cart_item.product_variant.product.available = False
        self.cart_item.product_variant.product.save()

        with self.assertRaises(ValidationError):
            CartItemFactory(
                cart=self.cart, product_variant=self.cart_item.product_variant
            )

    def test_cart_item_added_at(self):
        self.assertIsNotNone(self.cart_item.added_at)
        self.assertLess(self.cart_item.added_at, timezone.now())
