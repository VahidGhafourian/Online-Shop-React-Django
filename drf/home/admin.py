from typing import Any
from django.contrib import admin
from django.db.models.fields.json import JSONField
from django.db import models
from jsoneditor.forms import JSONEditor
from .models import Category, Product, ProductVariant #Order, OrderItem, Coupon, Payment
from .adminforms import DynamicProductForm, DynamicProductVariantForm
from django import forms


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'parent', 'slug')
    formfield_overrides = {
        JSONField: {
            "widget": JSONEditor(
                init_options={"mode": "code", "modes": ["view", "code", "tree"]},
            )
        }
    }

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'description')

    def get_form(self, request, obj=None, change=False, **kwargs):
        return DynamicProductForm

    def get_fieldsets(self, request, obj=None):
        # Start with the default fieldsets
        fieldsets = [
            (None, {'fields': ['title', 'slug', 'image', 'description', 'attributes']}),
        ]

        if obj:
            # Get the dynamic fields for the current product instance
            dynamic_fields = obj.get_dynamic_fields()
            # Append dynamic fields to the fieldsets
            if dynamic_fields:
                field_names = [field_name for field_name, _ in dynamic_fields]
                fieldsets.append((None, {'fields': field_names}))
        return fieldsets


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'items_count')
    # ordering = ['pk']
    def get_form(self, request, obj=None, change=False, **kwargs):
        return DynamicProductVariantForm


    def get_fieldsets(self, request, obj=None):
        # Start with the default fieldsets
        fieldsets = [
            (None, {'fields': ['product', 'price', 'items_count', 'attributes']}),
        ]

        if obj:
            # Get the dynamic fields for the current product instance
            dynamic_fields = obj.get_dynamic_fields()
            # Append dynamic fields to the fieldsets
            if dynamic_fields:
                field_names = [field_name for field_name, _ in dynamic_fields]
                fieldsets.append((None, {'fields': field_names}))
        return fieldsets


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductVariant, ProductVariantAdmin)


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'description')
#     formfield_overrides = {
#         JSONField: {
#             "widget": JSONEditor(
#                 init_options={"mode": "view", "modes": ["view", "code", "tree"]},
#             )
#         }
#     }

# class ProductVariantAdmin(admin.ModelAdmin):
#     list_display = ('product', 'price', 'items_count')
#     formfield_overrides = {
#         JSONField: {
#             "widget": JSONEditor(
#                 init_options={"mode": "view", "modes": ["view", "code", "tree"]},
#             )
#         }
#     }

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)





# admin.site.register(Category)

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     raw_id_fields = ('category', )

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
