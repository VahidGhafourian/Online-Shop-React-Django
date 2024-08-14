from rest_framework.test import APITestCase
from account.models import User, OtpCode, Address
from account.serializers import UserRegisterSerializer, OtpCodeSerializer, AddressSerializer

class UserSerializerTest(APITestCase):
    def setUp(self):
        self.user_data = {
            'phone_number': '+981234567899',
            'password': 'securepassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }
        # self.user = User.objects.create_user(**self.user_data)

    def test_user_serializer_valid(self):
        """Test UserRegisterSerializer with valid data."""
        serializer = UserRegisterSerializer(data=self.user_data)
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.phone_number, self.user_data['phone_number'])

    def test_user_serializer_password_mismatch(self):
        """Test UserRegisterSerializer with password mismatch."""
        data = self.user_data.copy()
        data['confirm_password'] = 'wrongpassword'
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('passwords must mach', str(serializer.errors))

class OtpCodeSerializerTest(APITestCase):
    def setUp(self):
        self.otp_data = {'phone_number': '+981234567890', 'code': '123456'}
        # self.otp = OtpCode.objects.create(**self.otp_data)

    def test_otp_serializer_valid(self):
        """Test OtpCodeSerializer with valid data."""
        serializer = OtpCodeSerializer(data=self.otp_data)
        self.assertTrue(serializer.is_valid())

class AddressSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number='+981234567890', password='securepassword')
        self.address_data = {
            'user': self.user.id,
            'is_default': True,
            'country': 'Iran',
            'state': 'Tehran',
            'city': 'Tehran',
            'street': '123 Main St',
            'postal_code': '123456'
        }
        # self.address = Address.objects.create(**self.address_data)

    def test_address_serializer_valid(self):
        """Test AddressSerializer with valid data."""
        serializer = AddressSerializer(data=self.address_data)
        self.assertTrue(serializer.is_valid())
