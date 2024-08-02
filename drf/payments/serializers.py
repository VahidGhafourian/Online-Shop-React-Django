from rest_framework import serializers
from .models import Payment, Transaction
from .models import Discount, Coupon

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'amount', 'status', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'payment', 'transaction_id', 'status', 'created_at']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'code', 'amount', 'is_active']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount', 'is_active']

class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField()
