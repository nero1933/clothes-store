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
        fields = ['id', 'name', 'url', 'is_main']


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
    product_rating = serializers.SerializerMethodField()
    # rating = serializers.FloatField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'brand', 'category',
                  'gender', 'attribute_options', 'product_items', 'product_rating', ]

    def get_product_rating(self, obj):
        if obj.product_rating:
            return round(obj.product_rating, 1)

        return None



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

    # def get_reviews(self, obj):
    #     reviews = []
    #     for product_item in obj.product_item.all():
    #         for product_variation in product_item.product_variation.all():
    #             for order_item in product_variation.order_item.all():
    #                 # Check if the order_item has a related review, otherwise continue
    #                 if hasattr(order_item, 'review') and order_item.review:
    #                     reviews.append(order_item.review)
    #
    #     return ReviewSerializer(reviews, many=True).data
