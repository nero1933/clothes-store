from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from ..models import Product, ProductVariation, ProductItem, Image, AttributeType, AttributeOption


class AttributeOptionSerializer(serializers.ModelSerializer):
    """
    Serializes 'id', 'name' and 'attribute_type' fields from 'AttributeOption' model
    for displaying them in 'ProductSerializer' serializer.
    """

    attribute_type = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = AttributeOption
        fields = ['id', 'name', 'attribute_type']


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializes 'id', 'name' and 'url' fields from 'Image' model
    for displaying them in 'ProductItemSerializer' serializer.
    """

    class Meta:
        model = Image
        fields = ['id', 'name', 'url']


class ProductVariationSerializer(serializers.ModelSerializer):
    """
    Serializes 'id', 'size' and 'qty_in_stock' fields from 'ProductVariation'
    model for displaying them in 'ProductItemSerializer' serializer.
    """

    size = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = ProductVariation
        fields = ['id', 'size', 'qty_in_stock']


class ProductItemSerializer(serializers.ModelSerializer):
    """
    Serializes several fields from 'ProductItem' model
    for displaying them in 'ProductSerializer' serializer.
    """

    # discount_price = serializers.SerializerMethodField()
    color = serializers.SlugRelatedField(slug_field='name', read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    product_variation = ProductVariationSerializer(many=True, read_only=True)
    price = serializers.IntegerField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductItem
        fields = ['id', 'product_code', 'price', 'color', 'image', 'product_variation']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class for 'Product' model.
    """

    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    attribute_option = AttributeOptionSerializer(many=True, read_only=True)
    product_item = ProductItemSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'brand', 'category', 'gender', 'attribute_option', 'product_item']
