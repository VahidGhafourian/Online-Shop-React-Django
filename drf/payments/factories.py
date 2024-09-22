import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Payment, Discount, Coupon
from orders.factories import OrderFactory
from products.factories import ProductVariantFactory, CategoryFactory
from django.utils import timezone
from datetime import timezone as tz


fake = Faker()

class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    order = factory.SubFactory(OrderFactory)
    amount = factory.Faker('random_int', min=1000, max=1000000)
    payment_method = factory.Iterator([choice[1] for choice in Payment.Method.choices])
    status = factory.Iterator([choice[0] for choice in Payment.Status.choices])
    timestamp = factory.LazyFunction(timezone.now)
    transaction_id = factory.Faker('uuid4')

class DiscountFactory(DjangoModelFactory):
    class Meta:
        model = Discount

    description = factory.Faker('sentence')
    discount_percent = factory.Faker('random_int', min=1, max=80)
    valid_from = factory.Faker('date_time_this_year', before_now=True, after_now=False, tzinfo=tz.utc)
    valid_to = factory.LazyAttribute(lambda o: timezone.now() + timezone.timedelta(days=1))
    is_active = True

    @factory.post_generation
    def applicable_to(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product_variant in extracted:
                self.applicable_to.add(product_variant)
        else:
            num_variants = fake.random_int(min=0, max=5)
            variants = ProductVariantFactory.create_batch(num_variants)
            self.applicable_to.add(*variants)

    @factory.post_generation
    def applicable_categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.applicable_categories.add(category)
        else:
            num_categories = fake.random_int(min=0, max=3)
            categories = CategoryFactory.create_batch(num_categories)
            self.applicable_categories.add(*categories)

class CouponFactory(DjangoModelFactory):
    class Meta:
        model = Coupon

    code = factory.Sequence(lambda n: f'COUPON{n:04d}')
    discount_percent = factory.Faker('random_int', min=1, max=80)
    valid_from = factory.Faker('date_time_this_year', before_now=True, after_now=False, tzinfo=tz.utc)
    valid_to = factory.LazyAttribute(lambda o: timezone.now() + timezone.timedelta(days=5))
    active = True
    usage_limit = factory.Faker('random_int', min=11, max=100)
    usage_count = factory.LazyAttribute(lambda o: fake.random_int(min=0, max=o.usage_limit-10))

    @factory.post_generation
    def applicable_to(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product_variant in extracted:
                self.applicable_to.add(product_variant)
        else:
            num_variants = fake.random_int(min=0, max=5)
            variants = ProductVariantFactory.create_batch(num_variants)
            self.applicable_to.add(*variants)

    @factory.post_generation
    def applicable_categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.applicable_categories.add(category)
        else:
            num_categories = fake.random_int(min=0, max=3)
            categories = CategoryFactory.create_batch(num_categories)
            self.applicable_categories.add(*categories)
