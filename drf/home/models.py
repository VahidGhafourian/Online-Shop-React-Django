from django.db import models
from django.urls import reverse
from account.models import User, Address
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    clproduct_attributes_schema = models.JSONField(default=dict, null=True, blank=True)
    variant_attributes_schema = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        ordering = ('title', )
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.DO_NOTHING, limit_choices_to={'children__isnull': True})
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True)
    description = RichTextField()
    attributes = models.JSONField(default=dict)
    # price = models.IntegerField()
    # quantity = models.IntegerField(default=1)
    # available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.slug, ])

class ProductVariant(models.Model):
    # id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    items_count = models.PositiveIntegerField()
    attributes = models.JSONField(default=dict, )

    def __str__(self):
        return f"{self.product.title} - Variant"


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     status = models.BooleanField(default=False)
#     transaction_id = models.CharField(max_length=255, null=True, default=None, unique=True)
#     discount = models.IntegerField(blank=True, null=True, default=None)
#     shipping_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name='orders')
#     is_send = models.BooleanField(default=False)
#     post_tracking_code = models.CharField(max_length=255, null=True, default=None, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ('status', '-updated_at')

#     def __str__(self):
#         return f'{self.user} - {str(self.id)}'

#     def get_total_price(self):
#         total = sum(item.get_cost() for item in self.items.all())
#         if self.discount:
#             discount_price = (self.discount / 100) * total
#             return int(total - discount_price)
#         return total

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.IntegerField()
#     quantity = models.IntegerField(default=1)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.id)

#     def get_cost(self):
#         return self.price * self.quantity

# class Coupon(models.Model):
#     code = models.CharField(max_length=30, unique=True)
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(80)])
#     active = models.BooleanField(default=False)

#     def __str__(self):
#         return self.code

# class Payment(models.Model):
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    # transaction_id = models.CharField(max_length=255, null=True, default=None, unique=True)
    # status = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f'{self.status} - {str(self.transaction_id)}'
