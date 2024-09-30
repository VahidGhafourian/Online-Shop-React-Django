from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from account.models import User, OtpCode, Address

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'phone_number': '1234567890',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'email_confirmed': True
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.phone_number, '1234567890')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)

    def test_user_str_method(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), '1234567890')

    def test_unique_email_constraint(self):
        User.objects.create_user(**self.user_data)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.user_data)

    def test_null_email_allowed(self):
        user1 = User.objects.create_user(phone_number='1111111111', password='test')
        user2 = User.objects.create_user(phone_number='2222222222', password='test')
        self.assertIsNone(user1.email)
        self.assertIsNone(user2.email)
        self.assertNotEqual(user1.pk, user2.pk)

class OtpCodeModelTest(TestCase):
    def setUp(self):
        self.otp_data = {
            'phone_number': '1234567890',
            'code': '12345',
            'expires_at': timezone.now() + timedelta(minutes=5)
        }

    def test_create_otp_code(self):
        otp = OtpCode.objects.create(**self.otp_data)
        self.assertEqual(OtpCode.objects.count(), 1)
        self.assertEqual(otp.phone_number, '1234567890')
        self.assertEqual(otp.code, '12345')

    def test_otp_str_method(self):
        otp = OtpCode.objects.create(**self.otp_data)
        self.assertTrue(str(otp).startswith('1234567890 - 12345 - '))

    def test_unique_phone_number_constraint(self):
        OtpCode.objects.create(**self.otp_data)
        with self.assertRaises(IntegrityError):
            OtpCode.objects.create(**self.otp_data)

class AddressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number='1234567890', password='testpassword')
        self.address_data = {
            'user': self.user,
            'country': 'USA',
            'state': 'California',
            'city': 'San Francisco',
            'street': '123 Test St',
            'postal_code': '94123',
            'is_default': True
        }

    def test_create_address(self):
        address = Address.objects.create(**self.address_data)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.postal_code, '94123')

    def test_address_str_method(self):
        address = Address.objects.create(**self.address_data)
        self.assertEqual(str(address), 'True - 94123 - 1234567890')

    def test_unique_default_address_constraint(self):
        Address.objects.create(**self.address_data)
        with self.assertRaises(IntegrityError):
            Address.objects.create(**self.address_data)

    def test_multiple_non_default_addresses_allowed(self):
        Address.objects.create(user=self.user, country='USA', postal_code='94123', is_default=False)
        Address.objects.create(user=self.user, country='USA', postal_code='94124', is_default=False)
        self.assertEqual(Address.objects.filter(user=self.user, is_default=False).count(), 2)
