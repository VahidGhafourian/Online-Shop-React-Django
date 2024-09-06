from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cart.factories import CartFactory, CartItemFactory
from account.factories import UserFactory
from products.factories import ProductVariantFactory
from cart.models import CartItem

class CartViewTest(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.cart = CartFactory(user=self.user)
        self.product_variant = ProductVariantFactory()
        self.cart_item = CartItemFactory(cart=self.cart, product_variant=self.product_variant)

    def test_get_cart(self):
        url = reverse('cart:cart-add-get')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_item_to_cart(self):
        url = reverse('cart:cart-add-get')
        data = {
            'product_variant': self.product_variant.id,
            'items_count': 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['items_count'], self.cart_item.items_count+2)

    def test_update_cart_item(self):
        url = reverse('cart:cart-item-edit', args=[self.cart_item.id])
        data = {
            'items_count': 5
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.items_count, 5)

    def test_delete_cart_item(self):
        url = reverse('cart:cart-item-edit', args=[self.cart_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 0)
