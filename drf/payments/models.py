from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from orders.models import Order
from products.models import Category, ProductVariant
from django.utils import timezone

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Waiting for payment'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
    class Method(models.TextChoices):
        CARD_TO_CARD = 'CARD_TO_CARD', 'Cart to cart'
        ONLINE_GATEWAY = 'ONLINE_GATEWAY', 'Online gateway payment'
        WALLET = 'WALLET', 'Wallet payment'
        CASH_ON_DELIVERY = 'CASH_ON_DELIVERY', 'Cash on delivery'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.PositiveBigIntegerField()
    payment_method = models.CharField(max_length=50, choices=Method.choices, default=Method.ONLINE_GATEWAY)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f'Payment for Order {self.order.id} {self.status=}'

class Discount(models.Model):
    description = models.TextField(blank=True)
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(80)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    applicable_to = models.ManyToManyField(ProductVariant, blank=True)
    applicable_categories = models.ManyToManyField(Category, blank=True)

    def calculate_discount(self, price):
        return price * (self.discount_percentage / 100)

    def __str__(self):
        return self.description

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(80)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=False)
    usage_limit = models.PositiveIntegerField(default=1)
    usage_count = models.PositiveIntegerField(default=0)
    applicable_to = models.ManyToManyField(ProductVariant, blank=True)
    applicable_categories = models.ManyToManyField(Category, blank=True)

    def is_valid(self):
        return self.is_active and self.usage_count < self.usage_limit and self.start_date <= timezone.now() <= self.end_date

    def calculate_discount(self, price):
        return price - (price * (self.discount_percentage / 100))

    def is_valid(self):
        now = timezone.now()
        return (
            self.active and
            self.valid_from <= now <= self.valid_to and
            self.usage_count < self.usage_limit
        )

    def __str__(self):
        return self.code
