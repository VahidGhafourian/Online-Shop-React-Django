from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from account.factories import AddressFactory, OtpCodeFactory, UserFactory
from account.models import Address, OtpCode, User


class UserCheckLoginPhoneTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("account:check_login_phone")
        self.user = UserFactory(phone_number="09123456789", password="testpass123")

    def test_existing_user_with_password(self):
        data = {"phone_number": "09123456789"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"new_user": False, "have_pass": True})

    def test_existing_user_without_password(self):
        self.user = User.objects.create(phone_number="09129876543")
        data = {"phone_number": "09129876543"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"new_user": False, "have_pass": False})

    def test_new_user(self):
        data = {"phone_number": "09987654321"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"new_user": True, "have_pass": False})

    def test_missing_phone_number(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GenerateSendOTPTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("account:send-otp")

    @patch("account.views.generate_otp")
    def test_generate_and_send_otp(self, mock_generate_otp):
        mock_generate_otp.return_value = "12345"
        data = {"phone_number": "09123456789"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["otp_code"], "12345")
        self.assertTrue(
            OtpCode.objects.filter(phone_number="09123456789", code="12345").exists()
        )

    def test_invalid_phone_number(self):
        data = {"phone_number": "invalid"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VerifyOTPTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("account:verify_otp")
        self.user = UserFactory(phone_number="09123456789", password="testpass123")
        self.otp = OtpCodeFactory(phone_number="09123456789", code="12345")

    def test_valid_otp(self):
        data = {"phone_number": "09123456789", "otp": "12345"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_otp(self):
        data = {"phone_number": "09123456789", "otp": "00000"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])

    def test_expired_otp(self):
        self.otp.expires_at = timezone.now() - timezone.timedelta(minutes=10)
        self.otp.save()
        data = {"phone_number": "09123456789", "otp": "12345"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])


class UserInfoViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.url = reverse("account:user-info")
        self.client.force_authenticate(user=self.user)

    def test_get_user_info(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], self.user.phone_number)

    def test_update_password(self):
        data = {"password": "newpassword123", "confirm_password": "newpassword123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_update_password_mismatch(self):
        data = {"password": "newpassword123", "confirm_password": "differentpassword"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])


class AddressViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.url = reverse("account:add-address")
        self.client.force_authenticate(user=self.user)

    def test_get_user_addresses(self):
        AddressFactory.create_batch(3, user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_add_address(self):
        data = {
            "is_default": True,
            "country": "Test Country",
            "state": "Test State",
            "city": "Test City",
            "street": "Test Street",
            "postal_code": "12345",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(Address.objects.first().user, self.user)

    def test_add_invalid_address(self):
        data = {"country": "Test Country"}  # Missing required fields
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
