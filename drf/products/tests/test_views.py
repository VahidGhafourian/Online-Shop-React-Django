from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Category, Product, ProductVariant, ProductImage
from products.factories import (
    CategoryFactory,
    ProductFactory,
    ProductVariantFactory,
    ProductImageFactory,
)
from account.factories import UserFactory

class CategoryViewTests(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.url_list = reverse('products:category-list')
        self.url_detail = reverse('products:category-detail', args=[self.category.id])

        self.staff_user = UserFactory(
            phone_number='staffuser',
            password='password123',
            is_staff=True,
        )

    def test_list_categories(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.category.id)

class ProductViewTests(APITestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.url_list = reverse('products:product-list')
        self.url_detail = reverse('products:product-detail', args=[self.product.id])
        self.staff_user = UserFactory(
            phone_number='staffuser',
            password='password123',
            is_staff=True,
        )

    # TODO: Add test if category is not currect

    def test_list_products(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product.id)
