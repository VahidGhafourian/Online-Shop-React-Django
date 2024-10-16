# your_app/providers.py
import random

from faker.providers import BaseProvider


class IranianPhoneNumberProvider(BaseProvider):
    def iranian_phone_number(self):
        return f"+98{random.randint(900, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
