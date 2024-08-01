from django.contrib import admin
from .models import Payment, Transaction, Coupon

admin.site.register(Payment)
admin.site.register(Transaction)
admin.site.register(Coupon)
