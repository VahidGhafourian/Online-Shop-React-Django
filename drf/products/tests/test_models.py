from django.test import TestCase
from products.models import Category, Product, ProductVariant, ProductImage

class CategoryModelTests(TestCase):
    def test_create_category(self):
        category = Category.objects.create(
            title='Electronics',
            slug='electronics',
        )
        self.assertEqual(str(category), 'Electronics')
        self.assertIsNone(category.parent)

    def test_category_parent_relationship(self):
        parent_category = Category.objects.create(
            title='Electronics',
            slug='electronics',
        )
        child_category = Category.objects.create(
            title='Mobile Phones',
            slug='mobile-phones',
            parent=parent_category,
        )
        self.assertEqual(child_category.parent, parent_category)
        self.assertEqual(parent_category.children.first(), child_category)


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Electronics', slug='electronics')

    def test_create_product(self):
        product = Product.objects.create(
            title='Smartphone',
            slug='smartphone',
            category=self.category,
            description='A modern smartphone.',
            available=True,
        )
        self.assertEqual(str(product), 'Smartphone')
        self.assertTrue(product.available)


class ProductVariantModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Electronics', slug='electronics')
        self.product = Product.objects.create(
            title='Smartphone',
            slug='smartphone',
            category=self.category,
            description='A modern smartphone.',
            available=True,
        )

    def test_create_product_variant(self):
        variant = ProductVariant.objects.create(
            product=self.product,
            price=999,
            items_count=10,
        )
        self.assertEqual(str(variant), f"{self.product.title} - Variant")
        self.assertEqual(variant.price, 999)


class ProductImageModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Electronics', slug='electronics')
        self.product = Product.objects.create(
            title='Smartphone',
            slug='smartphone',
            category=self.category,
            description='A modern smartphone.',
            available=True,
        )

    def test_create_product_image(self):
        image = ProductImage.objects.create(
            product=self.product,
            image='path/to/image.jpg',
            alt_text='An image of a smartphone',
        )
        self.assertEqual(str(image), f"Image of {self.product.title}")
        self.assertEqual(image.alt_text, 'An image of a smartphone')
