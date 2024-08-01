from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, null=True, unique=True)
    email_confirmd = models.EmailField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [] # This is jost for createsuperuser command.

    def __str__(self):
        return f'{self.last_name} - {self.email} - {self.phone_number}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'], condition=models.Q(email__isnull=False),
                name='unique_non_null_email'
            ),
        ]

class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, null=True, unique=True)
    # email = models.EmailField(max_length=255, null=True, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # models.UniqueConstraint(
            #     fields=['email'], condition=models.Q(email__isnull=False),
            #     name='unique_non_null_email_otp'
            # ),
            models.UniqueConstraint(
                fields=['phone_number'], condition=models.Q(phone_number__isnull=False),
                name='unique_non_null_phone_number_otp'
            ),
        ]

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'


class Address(models.Model):
    is_default = models.BooleanField(default=False)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','is_default'], condition=models.Q(is_default=True),
                name='unique_default_address'
            ),
        ]

    def __str__(self):
        return f'{self.is_default} - {self.postal_code} - {self.user}'
