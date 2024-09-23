from django.test import TestCase
from products.models import Category, Product, ProductVariant, ProductImage, Tag, Review, Inventory
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='Test Category',
            slug='test-category'
        )

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(self.category.__str__(), self.category.title)

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='Test Category',
        )
        self.product = Product.objects.create(
            category=self.category,
            title='Test Product',
            slug='test-product',
            description='Test description',
            available=True
        )

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(self.product.__str__(), self.product.title)

class ProductVariantModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            category=self.category,
            title='Test Product',
            slug='test-product',
            description='Test description',
            available=True
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            title='Test Variant',
            slug='test-variant',
            price=100
        )

    def test_variant_creation(self):
        self.assertTrue(isinstance(self.variant, ProductVariant))
        self.assertEqual(self.variant.__str__(), f"{self.product.title} - Variant")

class ProductImageModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            category=self.category,
            title='Test Product',
            slug='test-product',
            description='Test description',
            available=True
        )
        self.image = ProductImage.objects.create(
            product=self.product,
            alt_text='Test Image'
        )

    def test_image_creation(self):
        self.assertTrue(isinstance(self.image, ProductImage))
        self.assertEqual(self.image.__str__(), f"Image of {self.product.title}")

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(
            name='Test Tag',
            slug='test-tag'
        )

    def test_tag_creation(self):
        self.assertTrue(isinstance(self.tag, Tag))
        self.assertEqual(self.tag.__str__(), self.tag.name)

class ReviewModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            phone_number='09658456633',
            password='12345'
        )
        self.category = Category.objects.create(
            title='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            category=self.category,
            title='Test Product',
            slug='test-product',
            description='Test description',
            available=True
        )
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment='Test comment'
        )

    def test_review_creation(self):
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(self.review.__str__(), f"Review of {self.product.title} by {self.user.phone_number}")

class InventoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            category=self.category,
            title='Test Product',
            slug='test-product',
            description='Test description',
            available=True
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            title='Test Variant',
            slug='test-variant',
            price=100
        )
        self.inventory = Inventory.objects.create(
            product_variant=self.variant,
            quantity=10
        )

    def test_inventory_creation(self):
        self.assertTrue(isinstance(self.inventory, Inventory))
        self.assertEqual(self.inventory.__str__(), f"Inventory for {self.variant}")
