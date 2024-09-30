# Generated by Django 5.0.8 on 2024-09-30 06:52

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=13, unique=True)),
                ('code', models.CharField(max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone_number', models.CharField(max_length=13, unique=True)),
                ('password', models.CharField(max_length=128, null=True, verbose_name='password')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('last_notification_check', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_default', models.BooleanField(default=False)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='otpcode',
            constraint=models.UniqueConstraint(condition=models.Q(('phone_number__isnull', False)), fields=('phone_number',), name='unique_non_null_phone_number_otp'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(condition=models.Q(('email__isnull', False)), fields=('email',), name='unique_non_null_email'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(condition=models.Q(('email_confirmed', True)), fields=('email',), name='unique_confirmed_email'),
        ),
        migrations.AddConstraint(
            model_name='address',
            constraint=models.UniqueConstraint(condition=models.Q(('is_default', True)), fields=('user', 'is_default'), name='unique_default_address'),
        ),
    ]
