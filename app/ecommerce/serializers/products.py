from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .reviews import ReviewSerializer
from ..models import Product, ProductVariation, ProductItem, Image, AttributeOption, Discount


class DiscountSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the Discount object.
    """

    class Meta:
        model = Discount
        fields = '__all__'


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

    color = serializers.SlugRelatedField(slug_field='name', read_only=True)
    images = ImageSerializer(many=True, read_only=True, source='image')
    product_variations = ProductVariationSerializer(many=True, read_only=True, source='product_variation')
    price = serializers.IntegerField()
    discount_price = serializers.SerializerMethodField()
    discounts = DiscountSerializer(many=True, read_only=True, source='discount')

    class Meta:
        model = ProductItem
        fields = ['id', 'product_code', 'price', 'discount_price',
                  'color', 'images', 'discounts', 'product_variations']

    def get_discount_price(self, obj):
        return obj.get_discount_price()


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class for 'Product' model.
    """

    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    attribute_options = AttributeOptionSerializer(many=True, read_only=True, source='attribute_option')
    product_items = ProductItemSerializer(many=True, read_only=True, source='product_item')

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'brand', 'category',
                  'gender', 'attribute_options', 'product_items',]


class ProductDetailSerializer(ProductSerializer):
    """
    Displays values from 'Product' model and particular form 'ProductItem' model.
    Values are show in 'ProductAPIList' view.
    """

    reviews = ReviewSerializer(many=True, read_only=True, source='review')

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'brand', 'category',
                  'gender', 'attribute_options', 'product_items', 'reviews']
