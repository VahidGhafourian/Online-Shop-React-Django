import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Payment, Transaction, Discount, Coupon
from orders.factory import OrderFactory
from account.factory import UserFactory


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    order = factory.SubFactory(OrderFactory)
    amount = factory.Faker('random_number', digits=6)
    payment_method = factory.Faker('word')
    successful = factory.Faker('boolean')
    timestamp = factory.Faker('date_time_this_year')

class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    order = factory.SubFactory(OrderFactory)
    # payment = factory.SubFactory(PaymentFactory)  # Assuming a Transaction is linked to a Payment
    amount = factory.Faker('random_number', digits=6)
    transaction_id = factory.Faker('uuid4')
    timestamp = factory.Faker('date_time_this_year')
    status = factory.Faker('word')

class DiscountFactory(DjangoModelFactory):
    class Meta:
        model = Discount

    code = factory.Faker('word')
    description = factory.Faker('text', max_nb_chars=200)
    discount_percent = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True, min_value=0, max_value=100)
    valid_from = factory.Faker('date_time_this_year')
    valid_to = factory.Faker('date_time_this_year')
    active = factory.Faker('boolean')

class CouponFactory(DjangoModelFactory):
    class Meta:
        model = Coupon

    code = factory.Faker('word')
    discount = factory.Faker('random_int', min=0, max=80)
    valid_from = factory.Faker('date_time_this_year')
    valid_to = factory.Faker('date_time_this_year')
    active = factory.Faker('boolean')
