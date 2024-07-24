from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import viewsets

from ecommerce.models import Product


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
#    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.all()