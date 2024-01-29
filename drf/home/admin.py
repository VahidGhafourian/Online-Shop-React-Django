from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Coupon, Payment

admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category', )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated_at', 'status')
    list_filter = ('status',)

    inlines = (OrderItemInline,)


admin.site.register(Coupon)
admin.site.register(Payment)
