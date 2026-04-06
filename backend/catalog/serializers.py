from django.db import transaction
from rest_framework import serializers

from catalog.models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "is_primary"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "is_active"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock_quantity",
            "is_active",
            "category",
            "category_name",
            "images",
            "created_at",
            "updated_at",
        ]

    def validate_images(self, value):
        primary_count = sum(1 for image in value if image.get("is_primary"))
        if primary_count > 1:
            raise serializers.ValidationError("Only one primary image is allowed.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        images = validated_data.pop("images", [])
        product = super().create(validated_data)
        for image_data in images:
            ProductImage.objects.create(product=product, **image_data)
        return product

    @transaction.atomic
    def update(self, instance, validated_data):
        images = validated_data.pop("images", None)
        product = super().update(instance, validated_data)
        if images is not None:
            product.images.all().delete()
            for image_data in images:
                ProductImage.objects.create(product=product, **image_data)
        return product
