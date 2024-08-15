from django.test import TestCase
from rest_framework.exceptions import ValidationError
from products.models import Category, Product, ProductVariant, ProductImage
from products.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductVariantSerializer,
    ProductImageSerializer,
)

class CategorySerializerTests(TestCase):
    def test_category_serialization(self):
        category = Category.objects.create(title='Electronics', slug='electronics')
        serializer = CategorySerializer(category)
        expected_data = {
            'id': category.id,
            'title': 'Electronics',
            'slug': 'electronics',
            'parent': None,
            'product_attributes_schema': {},
            'variant_attributes_schema': {},
        }
        self.assertEqual(serializer.data, expected_data)

    def test_category_validation(self):
        serializer = CategorySerializer(data={'title': '', 'slug': ''})
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertIn('slug', serializer.errors)


class ProductSerializerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Electronics', slug='electronics')

    def test_product_serialization(self):
        product = Product.objects.create(
            title='Smartphone',
            slug='smartphone',
            category=self.category,
            description='A modern smartphone.',
            available=True,
        )
        serializer = ProductSerializer(product)
        expected_data = {
            'id': product.id,
            'title': 'Smartphone',
            'slug': 'smartphone',
            'category': self.category.id,
            'description': 'A modern smartphone.',
            'available': True,
            'attributes': {},
            # 'variants': [],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_product_validation(self):
        serializer = ProductSerializer(data={'title': '', 'slug': '', 'category': None})
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertIn('slug', serializer.errors)
        self.assertNotIn('category', serializer.errors)


class ProductVariantSerializerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Electronics', slug='electronics')
        self.product = Product.objects.create(
            title='Smartphone',
            slug='smartphone',
            category=self.category,
            description='A modern smartphone.',
            available=True,
        )

    def test_product_variant_serialization(self):
        variant = ProductVariant.objects.create(
            product=self.product,
            price=999,
            items_count=10,
        )
        serializer = ProductVariantSerializer(variant)
        expected_data = {
            'id': variant.id,
            'product': self.product.id,
            'price': 999,
            'items_count': 10,
            'attributes': {},
        }
        self.assertEqual(serializer.data, expected_data)

    def test_product_variant_validation(self):
        serializer = ProductVariantSerializer(data={'product': None, 'price': -10})
        self.assertFalse(serializer.is_valid())
        self.assertIn('product', serializer.errors)
        self.assertIn('price', serializer.errors)


class ProductImageSerializerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Electronics', slug='electronics')
        self.product = Product.objects.create(
            title='Smartphone',
            slug='smartphone',
            category=self.category,
            description='A modern smartphone.',
            available=True,
        )

    def test_product_image_serialization(self):
        image = ProductImage.objects.create(
            product=self.product,
            image='path/to/image.jpg',
            alt_text='An image of a smartphone',
        )
        serializer = ProductImageSerializer(image)
        expected_data = {
            'id': image.id,
            'product': self.product.id,
            'image': image.image.url,
            'alt_text': 'An image of a smartphone',
        }
        self.assertEqual(serializer.data, expected_data)

    def test_product_image_validation(self):
        serializer = ProductImageSerializer(data={'product': None, 'image': ''})
        self.assertFalse(serializer.is_valid())
        self.assertIn('product', serializer.errors)
        self.assertIn('image', serializer.errors)
