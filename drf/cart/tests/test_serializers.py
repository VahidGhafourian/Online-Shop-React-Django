from account.factories import UserFactory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from payments.factories import CouponFactory, DiscountFactory
from payments.models import Discount
from products.factories import CategoryFactory, ProductFactory, ProductVariantFactory
from rest_framework import status
from rest_framework.test import APITestCase

from cart.factories import CartFactory, CartItemFactory
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer


class CartItemSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.cart = Cart.objects.create(user=self.user)
        self.product_variant = ProductVariantFactory()
        self.cart_item = CartItemFactory(
            cart=self.cart, product_variant=self.product_variant
        )
        self.serializer = CartItemSerializer(instance=self.cart_item)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "id",
                "product_variant",
                "quantity",
                "price",
                "discounted_price",
                "subtotal",
            ],
        )

    def test_price_field_read_only(self):
        self.assertEqual(self.serializer.fields["price"].read_only, True)

    def test_discounted_price_calculation(self):
        category = CategoryFactory()
        product = ProductFactory(category=category)
        product_variant = ProductVariantFactory(product=product, price=1000)
        cart_item = CartItemFactory(
            cart=self.cart, product_variant=product_variant, quantity=2
        )

        # Create a discount
        discount = DiscountFactory(
            discount_percent=10, applicable_categories=[category]
        )
        serializer = CartItemSerializer(instance=cart_item)
        self.assertEqual(serializer.data["discounted_price"], 900)  # 1000 - 10%
        self.assertEqual(serializer.data["subtotal"], 1800)  # 900 * 2

    def test_validation_quantity_exceeds_stock(self):
        user = UserFactory()
        cart = Cart.objects.create(user=user)
        product_variant = ProductVariantFactory(create_inventory__quantity=1)
        data = {
            "cart": cart.id,
            "product_variant": product_variant.id,
            "quantity": product_variant.inventory.quantity + 1,
        }
        serializer = CartItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Requested quantity exceeds available stock.", str(serializer.errors)
        )

    def test_validation_product_not_available(self):
        product = ProductFactory(available=False)
        product_variant = ProductVariantFactory(product=product)

        data = {
            "cart": self.cart.id,
            "product_variant": product_variant.id,
            "quantity": 1,
        }
        serializer = CartItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Requested product is not available at the moment.", str(serializer.errors)
        )


class CartSerializerTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.cart = Cart.objects.create(user=self.user)
        self.product_variant1 = ProductVariantFactory(price=1000)
        self.product_variant2 = ProductVariantFactory(price=2000)
        self.cart_item1 = CartItemFactory(
            cart=self.cart,
            product_variant=self.product_variant1,
            quantity=2,
            price=self.product_variant1.price,
        )
        self.cart_item2 = CartItemFactory(
            cart=self.cart,
            product_variant=self.product_variant2,
            quantity=1,
            price=self.product_variant2.price,
        )
        self.serializer = CartSerializer(instance=self.cart)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "id",
                "items",
                "total_price",
                "total_discounted_price",
                "coupon",
                "final_price",
                "status",
                "created_at",
                "updated_at",
            ],
        )

    def test_items_field_contains_correct_data(self):
        self.assertEqual(len(self.serializer.data["items"]), 2)
        self.assertEqual(
            self.serializer.data["items"][0]["product_variant"],
            self.cart_item1.product_variant.id,
        )
        self.assertEqual(
            self.serializer.data["items"][1]["product_variant"],
            self.cart_item2.product_variant.id,
        )

    def test_total_price_calculation(self):
        self.assertEqual(
            self.serializer.data["total_price"], 4000
        )  # (1000 * 2) + (2000 * 1)

    def test_total_discounted_price_calculation(self):
        # Assuming no discounts
        self.assertEqual(self.serializer.data["total_discounted_price"], 4000)

    def test_final_price_with_coupon(self):
        coupon = CouponFactory(discount_percent=10)
        self.cart.coupon = coupon
        self.cart.save()
        serializer = CartSerializer(instance=self.cart)
        self.assertEqual(serializer.data["final_price"], 3600)  # 4000 - 10%

    def test_invalid_coupon_removal(self):
        coupon = CouponFactory(valid_to=timezone.now() - timezone.timedelta(days=1))
        self.cart.coupon = coupon
        self.cart.save()
        serializer = CartSerializer(instance=self.cart)
        self.assertIsNone(serializer.data["coupon"])

    def test_create_cart(self):
        url = reverse("cart:cart-add-get")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.last().user, self.user)
