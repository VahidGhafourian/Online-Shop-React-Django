from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from orders.factories import OrderFactory, OrderItemFactory
from account.factories import UserFactory
from orders.models import Order

class OrderViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.admin_user = UserFactory(is_staff=True, is_superuser=True)
        self.order = OrderFactory(user=self.user)
        self.admin_order = OrderFactory(items__size=1)  # This order is not associated with self.user

    def test_user_order_list_view(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('orders:user-order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one order for this user
        self.assertEqual(response.data[0]['id'], self.order.id)

    def test_admin_order_list_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('orders:all-order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both orders should be visible to admin

    def test_admin_order_detail_view(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('orders:order-detail', kwargs={'pk': self.order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)

    def test_admin_order_update(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('orders:order-detail', kwargs={'pk': self.order.id})
        data = {'status': Order.Status.SHIPPED}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Order.Status.SHIPPED)

    def test_admin_order_delete(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('orders:order-detail', kwargs={'pk': self.order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_admin_refund_order(self):
        self.client.force_authenticate(user=self.admin_user)
        order = OrderFactory(status=Order.Status.DELIVERED, items__have_items=False)
        OrderItemFactory(order=order, quantity=2)
        initial_quantity = order.items.first().product_variant.inventory.quantity

        url = reverse('orders:refound-order', kwargs={'pk': order.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.CANCELLED)
        self.assertEqual(
            order.items.first().product_variant.inventory.quantity,
            initial_quantity + 2
        )

    def test_admin_refund_order_invalid_status(self):
        self.client.force_authenticate(user=self.admin_user)
        order = OrderFactory(status=Order.Status.PENDING)

        url = reverse('orders:refound-order', kwargs={'pk': order.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PENDING)

    def test_unauthenticated_access(self):
        url = reverse('orders:user-order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_access_to_admin_views(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('orders:all-order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
