import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import User, Address, OtpCode
from .providers import IranianPhoneNumberProvider
from django.utils import timezone

fake = Faker()
fake.add_provider(IranianPhoneNumberProvider)

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    phone_number = factory.LazyAttribute(lambda _: fake.unique.iranian_phone_number())
    # password = factory.PostGenerationMethodCall('set_password', 'password123')
    email = factory.LazyFunction(lambda: fake.unique.email())
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_admin = False
    is_staff = False
    email_confirmd = False
    date_joined = factory.LazyFunction(timezone.now)
    date_updated = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        password = extracted if extracted else fake.password()
        obj.set_password(password)
        if create:
            obj.save()


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    is_default = False
    country = factory.Faker('country')
    state = factory.Faker('state')
    city = factory.Faker('city')
    street = factory.Faker('street_address')
    postal_code = factory.Faker('postcode')
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    user = factory.SubFactory(UserFactory)

class OtpCodeFactory(DjangoModelFactory):
    class Meta:
        model = OtpCode

    phone_number = factory.LazyAttribute(lambda _: fake.unique.iranian_phone_number())
    code = factory.Faker('random_int', min=10000, max=99999)
    created_at = factory.LazyFunction(timezone.now)
    expires_at = factory.LazyAttribute(lambda o: o.created_at + timezone.timedelta(minutes=5))
