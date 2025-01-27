from django.db.models import Prefetch, Avg

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from ecommerce.models import Product, ProductVariation, Review, Image, OrderItem, UserProfile
from ecommerce.serializers.products import ProductSerializer, ProductDetailSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        order_item_queryset = OrderItem.objects.only('id', 'product_variation_id')
        review_queryset = Review.objects.only('id', 'order_item_id', 'rating')
        image_queryset = Image.objects.filter(is_main=True)

        queryset = Product.objects \
            .select_related(
                'category',
                'brand'
            ) \
            .prefetch_related(
                'product_item',
                'product_item__color',
                Prefetch(
                    'product_item__image',
                    queryset=image_queryset
                ),
                'product_item__discount',
                Prefetch(
                    'product_item__product_variation',
                    queryset=ProductVariation.objects.filter(qty_in_stock__gt=0)
                ),
                'product_item__product_variation__size',
                Prefetch(
                    'product_item__product_variation__order_item',
                    queryset=order_item_queryset
                ),
                Prefetch(
                    'product_item__product_variation__order_item__review',
                    queryset=review_queryset
                ),
                'attribute_option',
                'attribute_option__attribute_type',
            ) \
            .annotate(product_rating=Avg('product_item__product_variation__order_item__review__rating'))

        return queryset

    def get_object(self):
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}

        obj = Product.objects \
            .select_related('category', 'brand') \
            .prefetch_related(
                'product_item',
                'product_item__color',
                'product_item__image',
                'product_item__discount',
                Prefetch(
                    'product_item__product_variation',
                    queryset=ProductVariation.objects.filter(qty_in_stock__gt=0)
                ),
                'product_item__product_variation__size',
                'attribute_option',
                'attribute_option__attribute_type',
                'review',
                Prefetch(
                    'review__user',
                    queryset=UserProfile.objects.only('id', 'first_name', 'last_name')
                ),
            ) \

        return get_object_or_404(obj, **filter_kwargs)

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'retrieve':
            serializer_class = ProductDetailSerializer

        return serializer_class
