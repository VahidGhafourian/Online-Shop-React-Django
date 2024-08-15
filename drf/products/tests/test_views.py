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

class CategoryViewTests(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.url_list = reverse('products:category-list')
        self.url_detail = reverse('products:category-detail', args=[self.category.id])

    def test_list_categories(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.category.id)

    def test_create_category(self):
        category_data = {
            'title': 'New Category',
            'slug': 'new-category',
            'product_attributes_schema': '{}',
            'variant_attributes_schema': '{}',
        }
        response = self.client.post(self.url_list, category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data['title'], category_data['title'])

    def test_update_category(self):
        updated_data = {'title': 'Updated Title'}
        response = self.client.put(self.url_detail, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.title, updated_data['title'])

    def test_delete_category(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())


class ProductViewTests(APITestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.url_list = reverse('products:product-list')
        self.url_detail = reverse('products:product-detail', args=[self.product.id])

    def test_list_products(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product.id)

    def test_create_product(self):
        category = CategoryFactory()
        product_data = {
            'title': 'New Product',
            'slug': 'new-product',
            'category': category.id,
            'description': 'Description of new product',
            'available': True,
            'attributes': '{}',
        }
        response = self.client.post(self.url_list, product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data['title'], product_data['title'])

    def test_update_product(self):
        updated_data = {'title': 'Updated Product Title'}
        response = self.client.put(self.url_detail, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, updated_data['title'])

    def test_delete_product(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())


class ProductVariantViewTests(APITestCase):
    def setUp(self):
        self.variant = ProductVariantFactory()
        self.url_list = reverse('products:product-variant-list')
        self.url_detail = reverse('products:product-variant-detail', args=[self.variant.id])

    def test_list_product_variants(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product_variant(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.variant.id)

    def test_create_product_variant(self):
        product = ProductFactory()
        variant_data = {
            'product': product.id,
            'price': 10000,
            'items_count': 50,
            'attributes': '{}',
        }
        response = self.client.post(self.url_list, variant_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductVariant.objects.count(), 2)
        self.assertEqual(response.data['price'], variant_data['price'])

    def test_update_product_variant(self):
        updated_data = {'price': 15000}
        response = self.client.put(self.url_detail, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.price, updated_data['price'])

    def test_delete_product_variant(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProductVariant.objects.filter(id=self.variant.id).exists())


class ProductImageViewTests(APITestCase):
    def setUp(self):
        self.image = ProductImageFactory()
        self.url_list = reverse('products:product-image-list')
        self.url_detail = reverse('products:product-image-detail', args=[self.image.id])

    def test_list_product_images(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product_image(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.image.id)

    def test_create_product_image(self):
        product = ProductFactory()
        image_data = {
            'product': product.id,
            'image': self.image.image.file,
            'alt_text': 'Sample Alt Text',
        }
        response = self.client.post(self.url_list, image_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductImage.objects.count(), 2)
        self.assertEqual(response.data['alt_text'], image_data['alt_text'])

    def test_update_product_image(self):
        updated_data = {'alt_text': 'Updated Alt Text'}
        response = self.client.put(self.url_detail, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.image.refresh_from_db()
        self.assertEqual(self.image.alt_text, updated_data['alt_text'])

    def test_delete_product_image(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProductImage.objects.filter(id=self.image.id).exists())
