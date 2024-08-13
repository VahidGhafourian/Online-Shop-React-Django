from rest_framework import serializers
from .models import Product, Category, ProductVariant # Order, OrderItem, Coupon, Payment
from account.models import Address
from account.serializers import AddressSerializer

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['id', 'order', 'product', 'price', 'quantity', 'created_at', 'updated_at']

# class CouponSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Coupon
#         fields = ['id', 'code', 'valid_from', 'valid_to', 'discount', 'active']

# class OrderSerializer(serializers.ModelSerializer):
#     total = serializers.SerializerMethodField()
#     class Meta:
#         model = Order
#         fields = '__all__'

#     def validate(self, data):
#         print('validate order')
#         print(data)
#         items = data.get('items', [])
#         for item_id, item_count in items:
#             product = Product.objects.get(id=item_id)
#             if product.quantity < item_count:
#                 raise serializers.ValidationError(f"Insufficient quantity for product {product.name}")
#         return data

#     def get_total(self, obj):
#         return obj.get_total_price()

#     def create(self, validated_data):
#         print('create order')
#         shipping_address_data = validated_data.pop('shipping_address')
#         items_data = validated_data.pop('items')
#         order = Order.objects.create(**validated_data)

#         # Creating related shipping address
#         shipping_address = Address.objects.create(order=order, **shipping_address_data)
#         order.shipping_address = shipping_address

#         # Creating related order items
#         for item_data in items_data:
#             OrderItem.objects.create(order=order, **item_data)

#         return order

# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = ['id', 'order', 'transaction_id', 'status', 'created_at', 'updated_at']