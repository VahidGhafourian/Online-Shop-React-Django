from account.models import User
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_attributes_schema = models.JSONField(default=dict, null=True, blank=True)
    variant_attributes_schema = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        # ordering = ('title', )
        verbose_name = "category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("home:category_filter", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"children__isnull": True},
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = RichTextField(null=True, blank=True)
    available = models.BooleanField(default=True)
    attributes = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField("Tag", related_name="products")

    # class Meta:
    # ordering = ('title', )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if not self.images.exists():
            ProductImage.objects.create(
                product=self, image="product_images/default.png"
            )

    @property
    def default_image(self):
        return self.images.first() or ProductImage(image="product_images/default.png")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "home:product_detail",
            args=[
                self.slug,
            ],
        )


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.PositiveIntegerField()
    attributes = models.JSONField(default=dict, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} - Variant"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    # TODO: Use external storage like MinIO
    image = models.ImageField(upload_to="product_images/")
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image of {self.product.title}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )  # 1-5 rating system
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approval = models.BooleanField(default=False)

    class Meta:
        unique_together = ("product", "user")  # Ensures one review per user per product

    def __str__(self):
        return f"Review of {self.product.title} by {self.user.phone_number}"


class Inventory(models.Model):
    product_variant = models.OneToOneField(
        ProductVariant, on_delete=models.CASCADE, related_name="inventory"
    )
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Inventory for {self.product_variant}"
