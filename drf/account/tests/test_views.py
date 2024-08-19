from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User, OtpCode, Address
from account.factories import UserFactory, AddressFactory
import random
import json

class UserCheckLoginPhoneTests(APITestCase):
    def setUp(self):
        self.existing_user = UserFactory(phone_number='09123456789')
        self.url = reverse('account:check_login_phone')

    def test_check_existing_phone_number(self):
        response = self.client.post(self.url, {'phoneNumber': self.existing_user.phone_number})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['newUser'], False)

    def test_check_new_phone_number(self):
        response = self.client.post(self.url, {'phoneNumber': '09111111111'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['newUser'], True)


class GenerateSendOTPTests(APITestCase):
    def setUp(self):
        self.url = reverse('account:send-otp')
        self.phone_number = '09123456789'

    def test_generate_and_send_otp(self):
        response = self.client.post(self.url, {'phoneNumber': self.phone_number})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'OTP sent successfully')

    def test_otp_creation_in_database(self):
        self.client.post(self.url, {'phoneNumber': self.phone_number})
        self.assertTrue(OtpCode.objects.filter(phone_number=self.phone_number).exists())


class VerifyOTPTests(APITestCase):
    def setUp(self):
        self.phone_number = '09123456789'
        self.otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.user = UserFactory(phone_number=self.phone_number)
        OtpCode.objects.create(phone_number=self.phone_number, code=self.otp_code)
        self.url = reverse('account:verify_otp')

    def test_verify_valid_otp(self):
        response = self.client.post(self.url, {'phone_number': self.phone_number, 'otp': self.otp_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_verify_invalid_otp(self):
        response = self.client.post(self.url, {'phone_number': self.phone_number, 'otp': '000000'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], 'Invalid OTP')


class UserInfoViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('account:user-info')
        self.client.force_authenticate(user=self.user)

    def test_get_user_info(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], self.user.phone_number)

    def test_update_user_password(self):
        response = self.client.post(self.url, {'password': 'newpassword', 'confirm_password': 'newpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Password updated successfully')

    def test_update_user_password_mismatch(self):
        response = self.client.post(self.url, {'password': 'newpassword', 'confirm_password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)


class AddressViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.address = AddressFactory(user=self.user)
        self.url = reverse('account:add-address')
        self.client.force_authenticate(user=self.user)

    def test_get_user_addresses(self):
        url = reverse('account:user-addresses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['postal_code'], self.address.postal_code)

    def test_add_new_address(self):
        newAddressForm = {
            'is_default': False,
            'country': 'Iran',
            'state': 'Tehran',
            'city': 'Tehran',
            'street': 'New Street',
            'postal_code': '123456',
        }
        response = self.client.post(self.url, newAddressForm)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['postal_code'], newAddressForm['postal_code'])

    def test_add_address_invalid_data(self):
        newAddressForm = {
            'is_default': False,
            'country': '',
            'state': 'Tehran',
            'city': 'Tehran',
            'street': 'New Street',
            'postal_code': '123456',
        }

        response = self.client.post(self.url, newAddressForm)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
