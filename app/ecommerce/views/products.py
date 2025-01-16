from django.db.models import Prefetch

from rest_framework import viewsets

from ecommerce.models import Product, ProductVariation
from ecommerce.serializers.products import ProductSerializer, ProductDetailSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'product_slug'

    def get_queryset(self):
        queryset = Product.objects \
            .select_related('category', 'brand') \
            .prefetch_related(
                'product_item',
                'product_item__color',
                'product_item__image',
                'product_item__discount',
                Prefetch(
                    'product_item__product_variation',
                    queryset=ProductVariation.objects.filter(qty_in_stock__gt=0)),
                'product_item__product_variation__size',
                'attribute_option',
                'attribute_option__attribute_type',
                'review',
            )

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'retrieve':
            serializer_class = ProductDetailSerializer

        return serializer_class
