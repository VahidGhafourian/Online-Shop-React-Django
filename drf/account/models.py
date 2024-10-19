from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=13, unique=True)
    password = models.CharField(_("password"), max_length=128, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, null=True)
    email_confirmed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    last_notification_check = models.DateTimeField(default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []  # This is just for createsuperuser command.

    def __str__(self):
        return f"{self.phone_number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(email__isnull=False),
                name="unique_non_null_email",
            ),
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(email_confirmed=True),
                name="unique_confirmed_email",
            ),
        ]


class Address(models.Model):
    is_default = models.BooleanField(default=False)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "is_default"],
                condition=models.Q(is_default=True),
                name="unique_default_address",
            ),
        ]

    def __str__(self):
        return f"{self.is_default} - {self.postal_code} - {self.user}"
