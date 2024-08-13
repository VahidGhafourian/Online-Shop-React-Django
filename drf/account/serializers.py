from rest_framework import serializers
from .models import User, OtpCode, Address


def clean_email(value):
    if 'admin' in value:
        raise serializers.ValidationError('admin cant be in admin')


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'password', 'confirm_password')

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': (clean_email,)}
        }

    def create(self, validated_data):
        del validated_data['confirm_password']
        return User.objects.get_or_create(**validated_data)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('passwords must mach')
        return data

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'date_joined')

class OtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = '__all__'

    def create(self, validated_data):
        return OtpCode.objects.create(**validated_data)

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'is_default', 'country', 'state', 'city', 'street', 'postal_code', 'created_at', 'updated_at', 'user']
