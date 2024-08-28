from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductVariantSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = serializers.ReadOnlyField(source='product_variant.product.title')
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product_variant', 'quantity', 'price']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be greater than or equal to one.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.phone_number')

    class Meta:
        model = Order
        fields = ['user', 'total_price', 'items', 'completed']

        extra_kwargs = {
            'total_price': {'read_only': True},
        }

    def create(self, validated_data):
        items_data = None
        if 'items' in validated_data:
            items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        if items_data:
          for item_data in items_data:
              OrderItem.objects.create(order=order, **item_data)
        return order


    def get_total_price(self, obj):
        return obj.get_total_price()
