from products.serializers import CategorySerializer, ProductVariantSerializer
from rest_framework import serializers

from .models import Coupon, Discount, Payment


class PaymentSerializer(
    serializers.ModelSerializer
):  # Adding format to the datetime fields
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "user", "order", "amount", "status", "created_at"]


class DiscountSerializer(serializers.ModelSerializer):
    applicable_to = ProductVariantSerializer(many=True, read_only=True)
    applicable_categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Discount
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    applicable_to = ProductVariantSerializer(many=True, read_only=True)
    applicable_categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Coupon
        fields = "__all__"
