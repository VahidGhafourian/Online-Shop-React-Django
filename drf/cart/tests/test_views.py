from account.factories import UserFactory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from payments.factories import CouponFactory
from products.factories import ProductVariantFactory
from rest_framework import status
from rest_framework.test import APITestCase

from cart.factories import CartFactory, CartItemFactory
from cart.models import Cart, CartItem


class CartViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.cart = Cart.objects.create(user=self.user)
        self.product_variant = ProductVariantFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_cart(self):
        url = reverse("cart:cart-review")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("items", response.data)

    def test_add_item_to_cart(self):
        url = reverse("cart:cart-add-get")
        data = {"product_variant": self.product_variant.id, "quantity": 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 2)

    def test_update_cart_item_quantity(self):
        cart_item = CartItemFactory(
            cart=self.cart, product_variant=self.product_variant, quantity=1
        )
        url = reverse("cart:cart-item-edit", kwargs={"item_id": cart_item.id})
        data = {"quantity": 3}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

    def test_remove_item_from_cart(self):
        cart_item = CartItemFactory(
            cart=self.cart, product_variant=self.product_variant
        )
        url = reverse("cart:cart-item-edit", kwargs={"item_id": cart_item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)


class ClearCartViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.cart = CartFactory(user=self.user)
        self.product_variant = ProductVariantFactory()
        CartItemFactory(cart=self.cart, product_variant=self.product_variant)
        self.client.force_authenticate(user=self.user)

    def test_clear_cart_items(self):
        url = reverse("cart:cart-clear")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_remove_coupon(self):
        coupon = CouponFactory()
        self.cart.coupon = coupon
        self.cart.save()
        url = reverse("cart:cart-clear")
        response = self.client.delete(f"{url}?action=remove_coupon")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertIsNone(self.cart.coupon)


class ApplyCouponViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.cart = CartFactory(user=self.user)
        self.product_variant = ProductVariantFactory()
        CartItemFactory(cart=self.cart, product_variant=self.product_variant)
        self.client.force_authenticate(user=self.user)
        self.coupon = CouponFactory(code="TEST10", discount_percent=10, active=True)
        self.coupon.applicable_to.add(self.product_variant)

    def test_apply_valid_coupon(self):
        url = reverse("cart:apply-coupon")
        data = {"coupon_code": "TEST10"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.coupon, self.coupon)

    def test_apply_invalid_coupon(self):
        url = reverse("cart:apply-coupon")
        data = {"coupon_code": "INVALID"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_apply_expired_coupon(self):
        self.coupon.valid_to = timezone.now() - timezone.timedelta(days=1)
        self.coupon.save()
        url = reverse("cart:apply-coupon")
        data = {"coupon_code": "TEST10"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_apply_coupon_when_one_already_applied(self):
        self.cart.coupon = CouponFactory()
        self.cart.save()
        url = reverse("cart:apply-coupon")
        data = {"coupon_code": "TEST10"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_apply_coupon_not_applicable_to_cart_items(self):
        self.coupon.applicable_to.clear()
        url = reverse("cart:apply-coupon")
        data = {"coupon_code": "TEST10"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
