from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_attributes_schema = models.JSONField(default=dict, null=True, blank=True)
    variant_attributes_schema = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        # ordering = ('title', )
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 limit_choices_to={'children__isnull': True})
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    # image = models.ImageField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    available = models.BooleanField(default=True)
    attributes = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
        # ordering = ('title', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.slug, ])


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    items_count = models.PositiveIntegerField()
    attributes = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.product.title} - Variant"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image of {self.product.name}"

# TODO: Tag, Review, Vendor, Inventory
