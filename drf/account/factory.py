import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import User, Address
from .providers import IranianPhoneNumberProvider

fake = Faker()
fake.add_provider(IranianPhoneNumberProvider)

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    phone_number = factory.LazyAttribute(lambda _: fake.iranian_phone_number())
    # phone_number = factory.Faker('phone_number', locale='fa_IR')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = factory.Faker('boolean', chance_of_getting_true=50)
    is_admin = factory.Faker('boolean', chance_of_getting_true=10)
    is_staff = factory.Faker('boolean', chance_of_getting_true=10)
    email_confirmd = factory.Faker('boolean', chance_of_getting_true=50)
    date_joined = factory.Faker('date_time_this_decade')
    date_updated = factory.Faker('date_time_this_decade')
    # password = factory.PostGenerationMethodCall('set_password', 'password123')

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        password = extracted if extracted else fake.password()
        obj.set_password(password)
        if create:
            obj.save()


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    is_default = factory.Faker('boolean')
    country = factory.Faker('country')
    state = factory.Faker('state')
    city = factory.Faker('city')
    street = factory.Faker('street_address')
    postal_code = factory.Faker('postcode')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    user = factory.SubFactory(UserFactory)
