from urllib.parse import urlsplit

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import resolve

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from ecommerce.models.orders import Order
from ecommerce.models.shopping_carts import ShoppingCartItem
from ecommerce.serializers.orders import OrderSerializer


class OrderCreateAPIView(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         GenericAPIView):

    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        shopping_cart_items = self.get_serializer_context()['shopping_cart_items']
        if not shopping_cart_items.exists():
            return Response({'error': 'No items in shopping cart.'}, status=status.HTTP_400_BAD_REQUEST)

        super().create(request, *args, **kwargs)
        # return redirect(reverse('orders-detail', kwargs={"pk": self.order_id}))
        return redirect(reverse('orders-detail', kwargs={"pk": self.request.session['order_id']}))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        context['shopping_cart_items'] = self.get_queryset()
        return context

    def perform_create(self, serializer):
        """
        Clear shopping cart after order is done.
        """
        order = serializer.save()
        self.request.session['order_id'] = order.pk
        # self.order_id = order.pk
        shopping_cart_items = self.get_serializer_context()['shopping_cart_items']
        shopping_cart_items.delete()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class OrderReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Check if the request came from a redirect
        if 'HTTP_REFERER' in request.META:
            referrer_url = request.META.get('HTTP_REFERER', '')
            referrer_path = urlsplit(referrer_url).path
            # Check if the redirect came from a 'create_order'
            if resolve(referrer_path).url_name == 'create_order':
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user) \
                .prefetch_related('order_item')
        else:
            return Order.objects.filter(pk=self.request.session['order_id']) \
                .prefetch_related('order_item')
