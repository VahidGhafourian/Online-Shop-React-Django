# your_app/providers.py
from faker.providers import BaseProvider
import random

class IranianPhoneNumberProvider(BaseProvider):
    def iranian_phone_number(self):
        return f'+98{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}'
