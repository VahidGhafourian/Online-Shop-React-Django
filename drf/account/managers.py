from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, email=None, first_name=None, last_name=None):
        if not phone_number:
            raise ValueError('User most have phone number')
        if not password:
            raise ValueError('User most have password')
        if email:
            email=self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, email=None, first_name=None, last_name=None):
        if email:
            email = self.normalize_email(email)
            if self.model.objects.filter(email=email).exists():
                raise ValueError('The email must be unique.')

        print(phone_number, password)
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
