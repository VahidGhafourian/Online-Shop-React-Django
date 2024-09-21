import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.utils import timezone
from django.utils.text import slugify
from .models import Category, Product, ProductVariant, ProductImage, Tag, Review, Inventory

fake = Faker()

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    parent = None
    title = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    product_attributes_schema = factory.LazyFunction(lambda: {'color': 'string', 'size': 'string'})
    variant_attributes_schema = factory.LazyFunction(lambda: {'color': 'string', 'size': 'string'})

    @factory.post_generation
    def parent(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.parent = extracted
        elif fake.boolean(chance_of_getting_true=30):
            self.parent = CategoryFactory()


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    title = factory.Faker('sentence', nb_words=3)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    description = factory.Faker('paragraph')
    available = True # factory.Faker('boolean', chance_of_getting_true=80)
    attributes = factory.LazyFunction(lambda: {'color': fake.color_name(), 'size': fake.random_element(['S', 'M', 'L', 'XL'])})
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

class ProductVariantFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    title = factory.LazyAttribute(lambda obj: f"{obj.product.title} - Variant {factory.Sequence(lambda n: n)}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    price = factory.Faker('random_int', min=1000, max=100000)  # Price in cents
    attributes = factory.LazyFunction(lambda: {'color': fake.color_name(), 'size': fake.random_element(['S', 'M', 'L', 'XL'])})

    @factory.post_generation
    def create_inventory(self, create, extracted, **kwargs):
        if create:
            InventoryFactory(product_variant=self)

class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)
    image = factory.django.ImageField(color=fake.color())
    alt_text = factory.Faker('sentence', nb_words=3)

class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for product in extracted:
                self.products.add(product)

class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory('account.factories.UserFactory')
    rating = factory.Faker('random_int', min=1, max=5)
    comment = factory.Faker('paragraph')
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    approval = factory.Faker('boolean', chance_of_getting_true=70)

class InventoryFactory(DjangoModelFactory):
    class Meta:
        model = Inventory

    product_variant = factory.SubFactory(ProductVariantFactory)
    quantity = factory.Faker('random_int', min=100, max=500)
