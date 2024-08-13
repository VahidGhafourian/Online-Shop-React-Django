from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from orders.models import Order
from account.models import User
from products.models import Category, ProductVariant
from time import timezone

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.PositiveBigIntegerField()
    payment_method = models.CharField(max_length=50)
    successful = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for Order {self.order.id} {self.status=}'

class Transaction(models.Model): #TODO: is this model ok? or we should give a foreignkey to payment?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Transaction {self.transaction_id}"

class Discount(models.Model):
    description = models.TextField(blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
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
        return price * (self.discount_percentage / 100)


    def __str__(self):
        return self.code
