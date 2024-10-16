from django.test import TestCase
from products.models import (
    Category,
    Product,
    ProductVariant,
    ProductImage,
    Tag,
    Review,
    Inventory,
)
from products.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductVariantSerializer,
    ProductImageSerializer,
    TagSerializer,
    ReviewSerializer,
    InventorySerializer,
)
from django.contrib.auth import get_user_model


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category_attributes = {
            "title": "Test Category",
            "slug": "test-category",
            "product_attributes_schema": {"type": "object"},
            "variant_attributes_schema": {"type": "object"},
        }
        self.category = Category.objects.create(**self.category_attributes)
        self.serializer = CategorySerializer(instance=self.category)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "id",
                    "parent",
                    "title",
                    "slug",
                    "created_at",
                    "updated_at",
                    "product_attributes_schema",
                    "variant_attributes_schema",
                ]
            ),
        )

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["title"], self.category_attributes["title"])
        self.assertEqual(data["slug"], self.category_attributes["slug"])


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category", slug="test-category"
        )
        self.product_attributes = {
            "category": self.category,
            "title": "Test Product",
            "slug": "test-product",
            "description": "Test description",
            "available": True,
            "attributes": {"color": "red"},
        }
        self.product = Product.objects.create(**self.product_attributes)
        self.serializer = ProductSerializer(instance=self.product)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "id",
                    "category",
                    "title",
                    "slug",
                    "description",
                    "available",
                    "attributes",
                    "images",
                    "default_image",
                    "variants",
                    "lowest_price",
                    "average_rating",
                    "created_at",
                    "updated_at",
                ]
            ),
        )

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["title"], self.product_attributes["title"])
        self.assertEqual(data["slug"], self.product_attributes["slug"])
        self.assertEqual(data["description"], self.product_attributes["description"])
        self.assertEqual(data["available"], self.product_attributes["available"])
        self.assertEqual(data["attributes"], self.product_attributes["attributes"])


class ProductVariantSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category", slug="test-category"
        )
        self.product = Product.objects.create(
            category=self.category, title="Test Product", slug="test-product"
        )
        self.variant_attributes = {
            "product": self.product,
            "title": "Test Variant",
            "slug": "test-variant",
            "price": 100,
            "attributes": {"size": "M"},
        }
        self.variant = ProductVariant.objects.create(**self.variant_attributes)
        self.serializer = ProductVariantSerializer(instance=self.variant)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()), set(["id", "product", "price", "quantity", "attributes"])
        )

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["price"], self.variant_attributes["price"])
        self.assertEqual(data["attributes"], self.variant_attributes["attributes"])


class ProductImageSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category", slug="test-category"
        )
        self.product = Product.objects.create(
            category=self.category, title="Test Product", slug="test-product"
        )
        self.image_attributes = {"product": self.product, "alt_text": "Test Image"}
        self.image = ProductImage.objects.create(**self.image_attributes)
        self.serializer = ProductImageSerializer(instance=self.image)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["id", "product", "image", "alt_text"]))

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["alt_text"], self.image_attributes["alt_text"])


class TagSerializerTest(TestCase):
    def setUp(self):
        self.tag_attributes = {"name": "Test Tag", "slug": "test-tag"}
        self.tag = Tag.objects.create(**self.tag_attributes)
        self.serializer = TagSerializer(instance=self.tag)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["id", "name", "slug", "products"]))

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.tag_attributes["name"])
        self.assertEqual(data["slug"], self.tag_attributes["slug"])


class ReviewSerializerTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            phone_number="09141548965", password="12345"
        )
        self.category = Category.objects.create(
            title="Test Category", slug="test-category"
        )
        self.product = Product.objects.create(
            category=self.category, title="Test Product", slug="test-product"
        )
        self.review_attributes = {
            "product": self.product,
            "user": self.user,
            "rating": 4,
            "comment": "Test comment",
        }
        self.review = Review.objects.create(**self.review_attributes)
        self.serializer = ReviewSerializer(instance=self.review)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "product", "user", "rating", "comment", "created_at"]),
        )

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["rating"], self.review_attributes["rating"])
        self.assertEqual(data["comment"], self.review_attributes["comment"])


class InventorySerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category", slug="test-category"
        )
        self.product = Product.objects.create(
            category=self.category, title="Test Product", slug="test-product"
        )
        self.variant = ProductVariant.objects.create(
            product=self.product, title="Test Variant", slug="test-variant", price=100
        )
        self.inventory_attributes = {"product_variant": self.variant, "quantity": 10}
        self.inventory = Inventory.objects.create(**self.inventory_attributes)
        self.serializer = InventorySerializer(instance=self.inventory)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["id", "product_variant", "quantity"]))

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["quantity"], self.inventory_attributes["quantity"])
