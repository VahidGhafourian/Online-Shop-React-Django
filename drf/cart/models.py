from django.db import models

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    items_count = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in cart of {self.cart.user.username}"

