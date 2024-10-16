from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self,
        phone_number,
        password,
        email=None,
        first_name=None,
        last_name=None,
        **extra_fields
    ):
        if not phone_number:
            raise ValueError("User most have phone number")
        if not password:
            raise ValueError("User most have password")
        if email:
            email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        phone_number,
        password,
        email=None,
        first_name=None,
        last_name=None,
        **extra_fields
    ):
        if email:
            email = self.normalize_email(email)
            if self.model.objects.filter(email=email).exists():
                raise ValueError("The email must be unique.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff = True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin = True")

        return self.create_user(
            phone_number, password, email, first_name, last_name, **extra_fields
        )
