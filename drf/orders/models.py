from django.db import models
from account.models import User
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    completed_at = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ('status', '-updated_at')

    def __str__(self):
        return f'Order {self.id} by user {str(self.user)}'

    # def get_total_price(self):
    #     total = sum(item.get_cost() for item in self.items.all())
    #     if self.discount:
    #         discount_price = (self.discount / 100) * total
    #         return int(total - discount_price)
    #     return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    # def get_cost(self):
    #     return self.price * self.quantity

# TODO: Shiping, Refund
