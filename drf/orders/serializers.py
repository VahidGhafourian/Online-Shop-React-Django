from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductVariantSerializer
from account.models import Address

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_variant.product.title', read_only=True)
        # Adding format to the datetime fields
    added_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'product_name', 'price', 'quantity', 'added_at']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be greater than or equal to one.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    total_price = serializers.SerializerMethodField()
    # user = serializers.StringRelatedField(source='user.phone_number')
    # Adding format to the datetime fields
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)
    shipping_address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'status', 'created_at', 'updated_at', 'shipping_address']

        extra_kwargs = {
            'total_price': {'read_only': True},
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items', None)
        shipping_address = validated_data.pop('shipping_address', None)
        order = Order.objects.create(shipping_address=shipping_address, **validated_data)
        if items_data:
          for item_data in items_data:
              OrderItem.objects.create(order=order, **item_data)
        return order

    def get_total_price(self, obj):
        return sum(item.get_cost() for item in obj.items.all())


class OrderAdminSerializer(OrderSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ['user_email']
