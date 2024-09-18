from rest_framework import serializers
from rest_framework import serializers
from .models import Category, Product, ProductVariant, ProductImage, Tag, Review, Inventory
import jsonschema

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'parent', 'title', 'slug',
            'product_attributes_schema', 'variant_attributes_schema'
        ]

    def validate_product_attributes_schema(self, value):
        try:
            jsonschema.validate(instance=value, schema={"type": "object"})
        except jsonschema.exceptions.ValidationError:
            raise serializers.ValidationError("Invalid JSON schema for product attributes")
        return value

    def validate_variant_attributes_schema(self, value):
        try:
            jsonschema.validate(instance=value, schema={"type": "object"})
        except jsonschema.exceptions.ValidationError:
            raise serializers.ValidationError("Invalid JSON schema for variant attributes")
        return value

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'id', 'product', 'image', 'alt_text'
        ]

class ProductVariantSerializer(serializers.ModelSerializer):
    quantity = serializers.ReadOnlyField(source='product_variant.inventory.quantity')
    class Meta:
        model = ProductVariant
        fields = [
            'id', 'product', 'price',
            'quantity', 'attributes'
        ]

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    lowest_price = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'title', 'slug', 'description', 'available',
            'attributes','images', 'variants', 'lowest_price', 'average_rating'
        ]

    def get_lowest_price(self, obj):
        variants = obj.variants.all()
        if variants:
            return min(variant.price for variant in variants)
        return None

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None

    def validate_attributes(self, value):
        category = self.instance.category if self.instance else self.initial_data.get('category')
        if category:
            schema = Category.objects.get(id=category).product_attributes_schema
            try:
                jsonschema.validate(instance=value, schema=schema)
            except jsonschema.exceptions.ValidationError:
                raise serializers.ValidationError("Product attributes do not match the category schema")
        return value
    # TODO: Add serializer for product list and product detail


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'products']


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(source='product.id')
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class InventorySerializer(serializers.ModelSerializer):
    product_variant = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'product_variant', 'quantity']


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
