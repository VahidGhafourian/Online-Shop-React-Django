from typing import Any

from django.contrib import admin
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor

from .adminforms import ProductAdminForm, ProductVariantAdminForm
from .models import (
    Category,
    Inventory,
    Product,
    ProductImage,
    ProductVariant,
    Review,
    Tag,
)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "slug", "parent")
    formfield_overrides = {
        JSONField: {
            "widget": JSONEditor(
                init_options={"mode": "code", "modes": ["view", "code", "tree"]},
            )
        }
    }


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    prepopulated_fields = {"slug": ("title",)}  # TODO: Add Persian to this feature.
    list_display = ("title", "category", "description")


class ProductVariantAdmin(admin.ModelAdmin):
    form = ProductVariantAdminForm
    list_display = ("id", "product", "price")
    # ordering = ['pk']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductImage)
admin.site.register(Inventory)
admin.site.register(Review)
admin.site.register(Tag)

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ('product',)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'updated_at', 'status')
#     list_filter = ('status',)

#     inlines = (OrderItemInline,)


# admin.site.register(Coupon)
# admin.site.register(Payment)
