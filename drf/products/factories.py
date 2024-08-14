import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Category, Product, ProductVariant, ProductImage

fake = Faker()

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    parent = None
    title = fake.word()
    slug = factory.LazyAttribute(lambda obj: fake.slug())
    created_at = factory.LazyFunction(fake.date_time_this_decade)
    updated_at = factory.LazyFunction(fake.date_time_this_decade)
    product_attributes_schema = factory.LazyAttribute(lambda x: {})
    variant_attributes_schema = factory.LazyAttribute(lambda x: {})

    @factory.post_generation
    def set_parent(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is None:
            depth = kwargs.get('depth', 0)
            if depth > 0:
                self.parent = CategoryFactory(depth=depth-1)

    class Params:
        with_parent = factory.Trait(
            parent=factory.SubFactory('products.factories.CategoryFactory')
        )


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    title = fake.word()
    slug = factory.LazyAttribute(lambda obj: fake.slug())
    description = fake.text(max_nb_chars=200)
    available = factory.Faker('boolean')
    attributes = factory.LazyAttribute(lambda x: {})
    created_at = factory.LazyFunction(fake.date_time_this_decade)
    updated_at = factory.LazyFunction(fake.date_time_this_decade)

class ProductVariantFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    price = factory.Faker('random_number', digits=5)
    items_count = factory.Faker('random_number', digits=3)
    attributes = factory.LazyAttribute(lambda x: {})

class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)
    image = factory.django.ImageField(color='blue')
    alt_text = fake.sentence(nb_words=6)
