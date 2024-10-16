import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from notifications.models import Notification
from notifications.serializers import NotificationSerializer

User = get_user_model()


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="1234567890", password="testpass123"
        )

    def test_notification_creation(self):
        notification = Notification.objects.create(
            user=self.user, notification_type="custom", message="Test notification"
        )
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(
            notification.__str__(),
            f"{self.user.phone_number} - custom - {notification.created_at}",
        )

    def test_notification_ordering(self):
        Notification.objects.create(
            user=self.user, notification_type="custom", message="Old notification"
        )
        timezone.now()
        new_notification = Notification.objects.create(
            user=self.user, notification_type="custom", message="New notification"
        )

        latest_notification = Notification.objects.first()
        self.assertEqual(latest_notification, new_notification)

    def test_notification_fields(self):
        notification = Notification.objects.create(
            user=self.user,
            notification_type="order_status",
            message="Your order status has changed",
        )
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.notification_type, "order_status")
        self.assertEqual(notification.message, "Your order status has changed")
        self.assertFalse(notification.is_read)
        self.assertIsNotNone(notification.created_at)


class NotificationSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="1234567890", password="testpass123"
        )
        self.notification_attributes = {
            "user": self.user,
            "notification_type": "custom",
            "message": "Test notification",
        }
        self.notification = Notification.objects.create(**self.notification_attributes)
        self.serializer = NotificationSerializer(instance=self.notification)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "id",
                "notification_type",
                "message",
                "is_read",
                "created_at",
                "content_type",
                "object_id",
            ],
        )

    def test_notification_type_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data["notification_type"], self.notification_attributes["notification_type"]
        )

    def test_message_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["message"], self.notification_attributes["message"])

    def test_is_read_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["is_read"], False)  # Default value

    def test_created_at_field_content(self):
        data = self.serializer.data
        self.assertIsNotNone(data["created_at"])


class NotificationViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            phone_number="1234567890", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)
        self.notification = Notification.objects.create(
            user=self.user, notification_type="custom", message="Test notification"
        )

    def test_list_notifications(self):
        response = self.client.get(reverse("notifications:notification-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_notification(self):
        response = self.client.get(
            reverse(
                "notifications:notification-detail", kwargs={"pk": self.notification.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Test notification")

    def test_delete_notification(self):
        response = self.client.delete(
            reverse(
                "notifications:notification-detail", kwargs={"pk": self.notification.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Notification.objects.count(), 0)

    def test_create_notification_not_allowed(self):
        response = self.client.post(reverse("notifications:notification-list"), data={})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_by_timeframe(self):
        Notification.objects.create(
            user=self.user,
            notification_type="custom",
            message="Old notification",
            created_at=timezone.now() - timezone.timedelta(days=7),
        )
        response = self.client.post(
            reverse("notifications:notification-get-by-timeframe"),
            data=json.dumps(
                {
                    "start_date": (
                        timezone.now() - timezone.timedelta(days=10)
                    ).isoformat(),
                    "end_date": timezone.now().isoformat(),
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both notifications should be included

    def test_get_by_timeframe_invalid_data(self):
        response = self.client.post(
            reverse("notifications:notification-get-by-timeframe"), data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get(reverse("notifications:notification-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
