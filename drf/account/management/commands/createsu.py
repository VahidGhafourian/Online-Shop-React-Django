from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "Create a superuser with environment variables"

    def handle(self, *args, **options):
        env_path = "./.env"
        load_dotenv(dotenv_path=env_path)
        User = get_user_model()
        if not User.objects.filter(
            phone_number=os.getenv("DJANGO_SUPERUSER_PHONENUMBER")
        ).exists():
            print(os.getenv("DJANGO_SUPERUSER_PHONENUMBER"))
            User.objects.create_superuser(
                phone_number=os.getenv("DJANGO_SUPERUSER_PHONENUMBER"),
                email=os.getenv("DJANGO_SUPERUSER_EMAIL"),
                password=os.getenv("DJANGO_SUPERUSER_PASSWORD"),
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))
