from django.db import models
from products.models import ProductVariant
from account.models import User
from django.core.exceptions import ValidationError
from payments.models import Coupon

class Cart(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ABANDONED = 'abandoned', 'Abandoned'
        CONVERTED = 'converted', 'Converted to Order'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"{self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product_variant')

    def __str__(self):
        return f"{self.product_variant.title} in cart {self.cart.id}"

    @property
    def subtotal(self):
        return self.quantity * self.price

    def clean(self):
        if self.quantity > self.product_variant.inventory.quantity:
            raise ValidationError("Requested quantity exceeds available stock.")
        if self.product_variant.product.available is False:
            raise ValidationError("Requested product is not available at the moment.")


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
