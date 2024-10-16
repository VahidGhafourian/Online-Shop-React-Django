from django.contrib.auth import get_user_model
from django.test import TestCase

from account.models import Address, OtpCode
from account.serializers import AddressSerializer, OtpCodeSerializer, UserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            "phone_number": "12345678901",
            "password": "testpassword",
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }
        self.user = User.objects.create(**self.user_data)

    def test_user_creation(self):
        serializer = UserSerializer(instance=self.user)
        serializer.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.phone_number, "12345678901")
        self.assertEqual(self.user.email, "test@example.com")

    def test_password_mismatch(self):
        self.user_data["confirm_password"] = "wrongpassword"
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("passwords must mach", str(serializer.errors))

    def test_email_validation(self):
        self.user_data["email"] = "admin@example.com"
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("admin cant be in admin", str(serializer.errors))

    def test_user_update(self):
        user = User.objects.create_user(
            phone_number="12345678902", password="oldpassword"
        )
        update_data = {"first_name": "Jane", "password": "newpassword"}
        serializer = UserSerializer(user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.first_name, "Jane")
        self.assertTrue(updated_user.check_password("newpassword"))


class OtpCodeSerializerTest(TestCase):
    def setUp(self):
        self.otp_data = {"phone_number": "12345678901", "code": "12345"}

    def test_otp_creation(self):
        serializer = OtpCodeSerializer(data=self.otp_data)
        self.assertTrue(serializer.is_valid())
        otp = serializer.save()
        self.assertEqual(OtpCode.objects.count(), 1)
        self.assertEqual(otp.phone_number, "12345678901")
        self.assertEqual(otp.code, "12345")
        self.assertIsNotNone(otp.expires_at)

    def test_invalid_phone_number(self):
        self.otp_data["phone_number"] = "123"
        serializer = OtpCodeSerializer(data=self.otp_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Phone number must be 11 digits", str(serializer.errors))

    def test_invalid_code(self):
        self.otp_data["code"] = "123"
        serializer = OtpCodeSerializer(data=self.otp_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("OTP code must be 5 digits", str(serializer.errors))


class AddressSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="12345678901", password="testpassword"
        )
        self.address_data = {
            "is_default": True,
            "country": "USA",
            "state": "California",
            "city": "San Francisco",
            "street": "123 Test St",
            "postal_code": "94123",
            "user": self.user.id,
        }

    def test_address_creation(self):
        serializer = AddressSerializer(data=self.address_data)
        self.assertTrue(serializer.is_valid())
        address = serializer.save()
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(address.country, "USA")
        self.assertEqual(address.user, self.user)

    def test_address_update(self):
        address = Address.objects.create(
            user=self.user, country="USA", state="California", city="Los Angeles"
        )
        update_data = {"city": "San Francisco", "postal_code": "94123"}
        serializer = AddressSerializer(address, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_address = serializer.save()
        self.assertEqual(updated_address.city, "San Francisco")
        self.assertEqual(updated_address.postal_code, "94123")
