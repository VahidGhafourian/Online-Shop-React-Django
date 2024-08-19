from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from orders.models import Order, OrderItem
from orders.factories import OrderFactory, OrderItemFactory
from account.factories import UserFactory
from products.factories import ProductVariantFactory

class OrderViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.order = OrderFactory(user=self.user)
        self.url_list = reverse('orders:order-list')
        self.url_detail = reverse('orders:order-detail', args=[self.order.id])

    def test_list_orders(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_order(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)

    def test_create_order(self):
        order_data = {
            'completed_at': False,
        }
        # print(self.client)
        response = self.client.post(self.url_list, order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(response.data['completed_at'], order_data['completed_at'])

    def test_update_order(self):
        updated_data = {'completed_at': True}
        response = self.client.put(self.url_detail, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertTrue(self.order.completed_at)

    def test_delete_order(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

class OrderItemViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.order_item = OrderItemFactory(order__user=self.user)
        self.url_list = reverse('orders:order-item-list')
        self.url_detail = reverse('orders:order-item-detail', args=[self.order_item.id])

    def test_list_order_items(self):
        response = self.client.get(self.url_list, {'order': self.order_item.order.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_order_item(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order_item.id)

    def test_create_order_item(self):
        product_variant = ProductVariantFactory()
        order_item_data = {
            'order': self.order_item.order.id,
            'product_variant': product_variant.id,
            'price': 100,
            'quantity': 2,
        }
        response = self.client.post(self.url_list, order_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 2)
        self.assertEqual(response.data['price'], order_item_data['price'])

    def test_update_order_item(self):
        updated_data = {'quantity': 5}
        response = self.client.put(self.url_detail, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.quantity, updated_data['quantity'])

    def test_delete_order_item(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(OrderItem.objects.filter(id=self.order_item.id).exists())
