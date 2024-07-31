import uuid

from django.db.models import Prefetch, F, Sum
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ecommerce.models import Discount
from ecommerce.models.shopping_carts import ShoppingCartItem
from ecommerce.serializers.shopping_carts import ShoppingCartItemSerializer


# from ..serializers.serializers_shopping_cart import ShoppingCartItemSerializer, ShoppingCartSerializer, \
#     ShoppingCartItemUpdateSerializer


class ShoppingCartItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartItemSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_queryset(self):
        queryset = ShoppingCartItem.objects \
            .select_related('cart',
                            'product_variation__size',
                            'product_variation__product_item__product',
                            ) \
            .prefetch_related('product_variation__product_item__discount')

        return queryset

    # def update(self, request, *args, **kwargs):
    #     return super().update(self, request, *args, **kwargs)

    # def get_serializer_class(self):
    #     serializer_class = self.serializer_class
    #     if self.action == 'update':
    #         serializer_class = ShoppingCartItemUpdateSerializer
    #
    #     return serializer_class


# class ShoppingCartAPIView(generics.ListAPIView):
#     permission_classes = (IsAuthenticated, )
#     serializer_class = ShoppingCartSerializer
#
#     def get_queryset(self):
#         return super().get_queryset()
