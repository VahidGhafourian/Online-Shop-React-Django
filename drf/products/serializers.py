import jsonschema
from django.utils.text import slugify
from rest_framework import serializers

from .models import (
    Category,
    Inventory,
    Product,
    ProductImage,
    ProductVariant,
    Review,
    Tag,
)


class CategorySerializer(serializers.ModelSerializer):
    # Adding format to the datetime fields
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "parent",
            "title",
            "slug",
            "created_at",
            "updated_at",
            "product_attributes_schema",
            "variant_attributes_schema",
        ]

    def validate_product_attributes_schema(self, value):
        try:
            jsonschema.validate(instance=value, schema={"type": "object"})
        except jsonschema.exceptions.ValidationError:
            raise serializers.ValidationError(
                "Invalid JSON schema for product attributes"
            )
        return value

    def validate_variant_attributes_schema(self, value):
        try:
            jsonschema.validate(instance=value, schema={"type": "object"})
        except jsonschema.exceptions.ValidationError:
            raise serializers.ValidationError(
                "Invalid JSON schema for variant attributes"
            )
        return value

    def create(self, validated_data):
        if "slug" not in validated_data or not validated_data["slug"]:
            validated_data["slug"] = slugify(validated_data["title"])
        return super().create(validated_data)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "alt_text"]


class ProductVariantSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ["id", "product", "price", "quantity", "attributes"]

    def get_quantity(self, obj):
        try:
            return obj.product_variant.inventory.quantity
        except AttributeError:
            return None


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    lowest_price = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    # Adding format to the datetime fields
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "title",
            "slug",
            "description",
            "available",
            "attributes",
            "images",
            "variants",
            "lowest_price",
            "average_rating",
            "created_at",
            "updated_at",
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
        category = (
            self.instance.category
            if self.instance
            else self.initial_data.get("category")
        )
        if category:
            schema = Category.objects.get(id=category).product_attributes_schema
            try:
                jsonschema.validate(instance=value, schema=schema)
            except jsonschema.exceptions.ValidationError:
                raise serializers.ValidationError(
                    "Product attributes do not match the category schema"
                )
        return value

    # TODO: Add serializer for product list and product detail

    def create(self, validated_data):
        if "slug" not in validated_data or not validated_data["slug"]:
            validated_data["slug"] = slugify(validated_data["title"])
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "products"]

    def create(self, validated_data):
        if "slug" not in validated_data or not validated_data["slug"]:
            validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.StringRelatedField(read_only=True)

    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "product", "user", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class InventorySerializer(serializers.ModelSerializer):
    product_variant = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Inventory
        fields = ["id", "product_variant", "quantity"]
