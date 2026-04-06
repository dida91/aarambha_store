from rest_framework import serializers

from catalog.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'sku',
            'price',
            'stock',
            'is_active',
            'images',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('price', 0) < 0:
            raise serializers.ValidationError({'price': 'Price cannot be negative.'})
        return attrs

    def _save_images(self, product, images_data):
        primary_count = sum(1 for i in images_data if i.get('is_primary'))
        if primary_count > 1:
            raise serializers.ValidationError({'images': 'Only one image can be primary.'})
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        self._save_images(product, images_data)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images_data is not None:
            instance.images.all().delete()
            self._save_images(instance, images_data)
        return instance
