import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.factories import (
    CategoryFactory, ProductFactory, ProductVariantFactory,
    ProductImageFactory, TagFactory, ReviewFactory, InventoryFactory
)
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import Category, Product, ProductVariant, ProductImage, Tag, Review, Inventory
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductListViewTest(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.product = ProductFactory(category=self.category)
        self.url = reverse('products:product-list')
        self.admin_user = User.objects.create_superuser('09010521833', 'password123')

    def test_get_product_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'category': self.category.id,
            'title': 'New Product',
            'description': 'A new product description',
            'available': True,
            'attributes': {'color': 'blue', 'size': 'M'}
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_get_product_detail(self):
        url = reverse('products:product-detail', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.product.title)

class ProductVariantListViewTest(APITestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.variant = ProductVariantFactory(product=self.product)
        self.url = reverse('products:product-variant-list')
        self.admin_user = User.objects.create_superuser('09010521833', 'password123')

    def test_get_variant_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_variant(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'product': self.product.id,
            'title': 'New Variant',
            'price': 1000,
            'attributes': {'color': 'red', 'size': 'L'}
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductVariant.objects.count(), 2)

class CategoryListViewTest(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.url = reverse('products:category-list')
        self.admin_user = User.objects.create_superuser('09010521833', 'password123')

    def test_get_category_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'title': 'New Category',
            'product_attributes_schema': {'color': 'string', 'size': 'string'},
            'variant_attributes_schema': {'color': 'string', 'size': 'string'}
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

class ProductImageListViewTest(APITestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.image = ProductImageFactory(product=self.product)
        self.url = reverse('products:product-image-list')
        self.admin_user = User.objects.create_superuser('09010521833', 'password123')

    def test_get_image_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class TagListViewTest(APITestCase):
    def setUp(self):
        self.tag = TagFactory()
        self.url = reverse('products:tag-list')
        self.admin_user = User.objects.create_superuser('09010521833', 'password123')

    def test_get_tag_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_tag(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'New Tag',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 2)

class InventoryViewTest(APITestCase):
    def setUp(self):
        self.product_variant = ProductVariantFactory(create_inventory__create_inventory=False)
        self.inventory = InventoryFactory(product_variant=self.product_variant)
        self.url = reverse('products:inventory-detail', kwargs={'product_variant_id': self.product_variant.id})
        self.admin_user = User.objects.create_superuser('09010521833', 'password123')

    def test_get_inventory(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], self.inventory.quantity)

    def test_update_inventory(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'quantity': 50
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 50)

class ReviewViewTest(APITestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.review = ReviewFactory(product=self.product)
        self.url = reverse('products:review-list', kwargs={'product_id': self.product.id})
        self.admin_user = User.objects.create_superuser('09010521833', 'password123')

    def test_get_reviews(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_review(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'product': self.product.id,
            'rating': 2,
            'comment': 'Great product!',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
