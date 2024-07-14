from django.contrib import admin
from .models import Category, Product, ProductVariant #Order, OrderItem, Coupon, Payment


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'parent', 'slug')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description')

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'items_count')

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
