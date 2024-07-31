from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ecommerce.models.shopping_carts import ShoppingCartItem, ShoppingCart
from ecommerce.serializers.shopping_carts import ShoppingCartItemSerializer



class ShoppingCartItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartItemSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_queryset(self):
        queryset = ShoppingCartItem.objects \
            .select_related('cart',
                            'cart__user',
                            'product_variation__size',
                            'product_variation__product_item__product',
                            ) \
            .prefetch_related('product_variation__product_item__discount',) \
            .filter(cart__user=self.request.user)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'create':
            context['cart_items'] = ShoppingCartItem.objects \
                .select_related('product_variation') \
                .filter(cart__user=self.request.user)
            context['cart'] = ShoppingCart.objects \
                .get(user=self.request.user)

        return context
