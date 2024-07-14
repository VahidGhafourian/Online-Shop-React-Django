from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Category
from account.models import User

class ProductTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Electronics", slug="electronics")
        self.product = Product.objects.create(
            title="Laptop",
            description="A powerful laptop",
            category=self.category,
            attributes={"color": "black"}
        )
        self.user = User.objects.create_user(phone_number='09121222121', password='testpassword')
        self.client.login(phone_number='09121222121', password='testpassword')

    def test_get_products(self):
        url = reverse('get_products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_detail(self):
        url = reverse('product_detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
