from rest_framework import serializers

from .models import Address, User


def clean_email(value):
    if "admin" in value:
        raise serializers.ValidationError("admin cant be in admin")


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "password",
            "confirm_password",
            "last_login",
            "first_name",
            "last_name",
            "is_active",
            "is_admin",
            "email_confirmed",
            "date_joined",
            "date_updated",
            "email",
            "phone_number",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": (clean_email,)},
            "is_admin": {"read_only": True},
            "is_active": {"read_only": True},
            "last_login": {"read_only": True},
            "date_joined": {"read_only": True},
            "phone_number": {"read_only": True},
            "date_updated": {"read_only": True},
            "email_confirmed": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        password = validated_data.pop("password", None)

        user, created = User.objects.get_or_create(validated_data)
        if created:
            if password:
                user.set_password(password)
            user.save()
        return user

    def validate(self, data):
        if (
            "password" in data
            and "confirm_password" in data
            and data["password"] != data["confirm_password"]
        ):
            raise serializers.ValidationError("passwords must mach")
        return data

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        for attr, value in validated_data.items():
            if attr != "password":
                setattr(instance, attr, value)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])

        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "is_default",
            "country",
            "state",
            "city",
            "street",
            "postal_code",
            "user",
        ]
