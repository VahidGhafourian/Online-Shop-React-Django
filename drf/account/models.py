from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, null=True, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [] # This is jost for createsuperuser command.

    def __str__(self):
        return f'{self.last_name} - {self.email} - {self.phone_number}'

    def is_staff(self):
        return self.is_staff

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'], condition=models.Q(email__isnull=False),
                name='unique_non_null_email'
            ),
        ]

class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
