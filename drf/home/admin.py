from django.contrib import admin
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from .models import Category, Product, ProductVariant #Order, OrderItem, Coupon, Payment


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'parent', 'slug')
    formfield_overrides = {
        JSONField: {
            "widget": JSONEditor(
                init_options={"mode": "view", "modes": ["view", "code", "tree"]},
            )
        }
    }
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description')
    formfield_overrides = {
        JSONField: {
            "widget": JSONEditor(
                init_options={"mode": "view", "modes": ["view", "code", "tree"]},
            )
        }
    }

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'items_count')
    formfield_overrides = {
        JSONField: {
            "widget": JSONEditor(
                init_options={"mode": "view", "modes": ["view", "code", "tree"]},
            )
        }
    }

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
