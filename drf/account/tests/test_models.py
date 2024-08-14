from django.test import TestCase
from account.models import User, OtpCode, Address
from django.db.utils import IntegrityError

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='+981234567890',
            password='securepassword',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )

    def test_user_creation(self):
        """Test user creation and string representation."""
        self.assertEqual(self.user.phone_number, '+981234567890')
        self.assertEqual(self.user.email, 'john.doe@example.com')
        self.assertEqual(str(self.user), 'Doe - john.doe@example.com - +981234567890')

    def test_unique_email_constraint(self):
        """Test unique email constraint."""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                phone_number='+981234567891',
                password='anotherpassword',
                email='john.doe@example.com'
            )

class OtpCodeModelTest(TestCase):
    def setUp(self):
        self.otp = OtpCode.objects.create(phone_number='+981234567890', code='123456')

    def test_otp_creation(self):
        """Test OTP creation and string representation."""
        self.assertEqual(self.otp.phone_number, '+981234567890')
        self.assertEqual(self.otp.code, '123456')
        self.assertIn('123456', str(self.otp))

class AddressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='+981234567890',
            password='securepassword'
        )
        self.address = Address.objects.create(
            user=self.user,
            is_default=True,
            country='Iran',
            state='Tehran',
            city='Tehran',
            street='123 Main St',
            postal_code='123456'
        )

    def test_address_creation(self):
        """Test address creation and string representation."""
        self.assertEqual(self.address.country, 'Iran')
        self.assertEqual(self.address.city, 'Tehran')
        self.assertIn('123456', str(self.address))

    def test_unique_default_address_constraint(self):
        """Test unique default address constraint."""
        with self.assertRaises(IntegrityError):
            Address.objects.create(
                user=self.user,
                is_default=True,
                country='Iran',
                state='Tehran',
                city='Tehran',
                street='456 Elm St',
                postal_code='654321'
            )
