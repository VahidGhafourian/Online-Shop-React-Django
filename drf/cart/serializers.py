from django.db import models
from django.utils import timezone
from payments.models import Discount
from payments.serializers import CouponSerializer
from products.models import ProductVariant
from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.IntegerField(min_value=0, read_only=True)
    discounted_price = serializers.IntegerField(min_value=0, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "product_variant",
            "quantity",
            "price",
            "discounted_price",
            "subtotal",
        ]

        extra_kwargs = {
            "cart": {"write_only": True},
            "price": {"read_only": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        discounted_price = self.get_discounted_price(instance)
        representation["discounted_price"] = discounted_price
        representation["subtotal"] = discounted_price * instance.quantity
        return representation

    def get_discounted_price(self, instance):
        product_variant = instance.product_variant
        original_price = product_variant.price

        # Check for applicable discounts
        discounts = Discount.objects.filter(
            models.Q(applicable_to=product_variant)
            | models.Q(applicable_categories=product_variant.product.category),
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_to__gte=timezone.now(),
        ).order_by(
            "-discount_percent"
        )  # Get the highest discount

        if discounts.exists():
            discount = discounts.first()
            discounted_price = original_price * (1 - discount.discount_percent / 100)
            return max(discounted_price, 0)  # Ensure price doesn't go below 0

        return original_price

    def validate_product_variant(self, product_variant):
        if product_variant.product.available is False:
            raise serializers.ValidationError(
                "Requested product is not available at the moment."
            )
        return product_variant

    def validate_quantity(self, quantity):
        instance = self.instance
        if instance:
            product_variant = instance.product_variant
        else:
            product_variant = self.initial_data.get("product_variant")
            try:
                product_variant = ProductVariant.objects.get(pk=product_variant)
            except ProductVariant.DoesNotExist:
                raise serializers.ValidationError("Invalid product variant.")

        if quantity > product_variant.inventory.quantity:
            raise serializers.ValidationError(
                "Requested quantity exceeds available stock."
            )
        return quantity

    def create(self, validated_data):
        validated_data["price"] = validated_data["product_variant"].price
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "product_variant" in validated_data:
            instance.price = validated_data["product_variant"].price
        return super().update(instance, validated_data)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, allow_null=True, required=False)
    total_price = serializers.IntegerField(min_value=0, read_only=True)
    total_discounted_price = serializers.IntegerField(min_value=0, read_only=True)
    final_price = serializers.IntegerField(min_value=0, read_only=True)
    coupon = CouponSerializer(read_only=True)
    status = serializers.ChoiceField(choices=Cart.Status.choices, read_only=True)

    # Adding format to the datetime fields
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_price",
            "total_discounted_price",
            "coupon",
            "final_price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total_price = sum(
            item.product_variant.price * item.quantity for item in instance.items.all()
        )
        total_discounted_price = sum(
            self.fields["items"].child.get_discounted_price(item) * item.quantity
            for item in instance.items.all()
        )

        representation["total_price"] = total_price
        representation["total_discounted_price"] = total_discounted_price

        final_price = total_discounted_price
        if instance.coupon and instance.coupon.is_valid():
            final_price *= 1 - instance.coupon.discount_percent / 100
        else:
            # Remove invalid coupon from cart
            instance.coupon = None
            instance.save()

        representation["final_price"] = max(
            final_price, 0
        )  # Ensure price doesn't go below 0
        return representation

    def create(self, validated_data):
        user = self.context["request"].user
        return Cart.objects.create(user=user, **validated_data)
