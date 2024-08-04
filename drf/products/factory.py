import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Category, Product, ProductVariant, ProductImage 

fake = Faker()

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    parent = factory.SubFactory('myapp.factories.CategoryFactory', null=True, blank=True)
    title = factory.Faker('word')
    slug = factory.Faker('slug')
    created_at = factory.Faker('date_time_this_decade')
    updated_at = factory.Faker('date_time_this_decade')
    product_attributes_schema = factory.Faker('pydict', number_of_items=3)
    variant_attributes_schema = factory.Faker('pydict', number_of_items=3)

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory, null=True)
    title = factory.Faker('word')
    slug = factory.Faker('slug')
    description = factory.Faker('text', max_nb_chars=200)
    available = factory.Faker('boolean')
    attributes = factory.Faker('pydict', number_of_items=3)
    created_at = factory.Faker('date_time_this_decade')
    updated_at = factory.Faker('date_time_this_decade')

class ProductVariantFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    price = factory.Faker('pydecimal', left_digits=6, right_digits=2, positive=True, min_value=1, max_value=1000)
    items_count = factory.Faker('random_int', min=1, max=100)
    attributes = factory.Faker('pydict', number_of_items=3)

class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)
    image = factory.django.ImageField(filename='default_image.jpg')
    alt_text = factory.Faker('sentence', nb_words=6)
