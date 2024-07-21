from django.db import models
from django.urls import reverse
from account.models import User, Address
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator
from jsonschema import validate, ValidationError
from django import forms

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_attributes_schema = models.JSONField(default=dict, null=True, blank=True)
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
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, limit_choices_to={'children__isnull': True})
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    # available = models.BooleanField(default=True)
    attributes = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title

    def validate_attributes(self):
        a = validate(instance=self.attributes, schema=self.category.product_attributes_schema)
        print(a)

    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.slug, ])

    def get_dynamic_fields(self):
        """
        Returns a list of form fields based on the attributes JSON field.
        """
        fields = []
        attributes_schema = self.category.product_attributes_schema or {}
        def create_field(name, field_type, label):
            if field_type == 'string':
                return forms.CharField(label=label)
            elif field_type == 'number':
                return forms.FloatField(label=label)
            elif field_type == 'integer':
                return forms.IntegerField(label=label)
            elif field_type == 'boolean':
                return forms.BooleanField(label=label)
            elif field_type == 'object':
                return forms.CharField(label=label, widget=forms.Textarea)  # For nested objects, you might need a custom widget
            # Add more field types as needed
            return forms.CharField(label=label)  # Default to CharField if type is unknown

        def process_schema(schema, prefix='attributes_'):
            properties = schema.get('properties', {})
            for field, field_attrs in properties.items():
                field_type = field_attrs.get('type')
                field_label = field_attrs.get('title', field)
                field_name = f'{prefix}{field}'

                fields.append((field_name, create_field(field_name, field_type, field_label)))

                if field_type == 'object':
                    process_schema(field_attrs, prefix=f'{field_name}_')

        process_schema(attributes_schema)
        return fields

class ProductVariant(models.Model):
    # id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    items_count = models.PositiveIntegerField()
    attributes = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.product.title} - Variant"

    def get_dynamic_fields(self):
        """
        Returns a list of form fields based on the attributes JSON field.
        """
        fields = []
        attributes_schema = self.product.category.variant_attributes_schema or {}
        def create_field(name, field_type, label):
            if field_type == 'string':
                return forms.CharField(label=label)
            elif field_type == 'number':
                return forms.FloatField(label=label)
            elif field_type == 'integer':
                return forms.IntegerField(label=label)
            elif field_type == 'boolean':
                return forms.BooleanField(label=label)
            elif field_type == 'object':
                return forms.CharField(label=label, widget=forms.Textarea)  # For nested objects, you might need a custom widget
            # Add more field types as needed
            return forms.CharField(label=label)  # Default to CharField if type is unknown

        def process_schema(schema, prefix='attributes_'):
            properties = schema.get('properties', {})
            for field, field_attrs in properties.items():
                field_type = field_attrs.get('type')
                field_label = field_attrs.get('title', field)
                field_name = f'{prefix}{field}'

                fields.append((field_name, create_field(field_name, field_type, field_label)))

                if field_type == 'object':
                    process_schema(field_attrs, prefix=f'{field_name}_')

        process_schema(attributes_schema)
        return fields

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
