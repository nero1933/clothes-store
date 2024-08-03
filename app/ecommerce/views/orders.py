import secrets
import string

from urllib.parse import urlsplit

from django.urls import resolve

from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.generics import GenericAPIView, CreateAPIView

from ecommerce.models import UserProfile
from ecommerce.models.orders import Order, OrderItem
from ecommerce.models.shopping_carts import ShoppingCartItem
from ecommerce.serializers.orders import OrderSerializer


class OrderCreateAPIView(CreateAPIView):
    """
    1 post,
    2 create,
    3 get_serializer_context,
    4 perform_create,
    5 serializer.save(),
    6 Response
    """

    # 1. Guest -> to -> User
    # 2. Shopping cart items -> to -> Order items
    # 3. Calculate order price and set context['price']
    # 4. Retrieve address and set context['address']
    # 5. Create Order

    is_authenticated = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = ShoppingCartItem.objects \
            .select_related('cart__user',
                            'product_variation',
                            'product_variation__product_item') \
            .prefetch_related('cart__user__address',
                              'product_variation__product_item__discount') \
            .filter(cart__user=self.request.user, cart__user__address=self.request.user)

        return queryset

    def prepare_order_items(self) -> list[OrderItem]:
        cart_items = ShoppingCartItem.objects \
            .prefetch_related('product_variation__product_item__discount') \
            .filter(cart__user=self.request.user)

        bulk_list = []

        for cart_item in cart_items:
            order_item_price = (cart_item.product_variation.product_item.get_discount_price() * cart_item.quantity)
            bulk_list.append(
                OrderItem(
                    product_variation=cart_item.product_variation,
                    quantity=cart_item.quantity,
                    price=order_item_price,
                )
            )

        return bulk_list


    def post(self, request, *args, **kwargs):
        """
        Test
        """
        customer = request.user

        # Order serializer requires email.
        # If user isn't a guest than add
        # his email to self.request.data['email']


        serializer = self.get_serializer(data=request.data)

        order_items = self.prepare_order_items()
        order_price = sum(map(lambda x: x.price, order_items))
        serializer.context['order_price'] = order_price

        serializer.is_valid(raise_exception=True)

        if customer.is_guest: # if guest
            new_email = serializer.validated_data['email']
            customer.guest_to_user(new_email)
        #
        #
        #
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)


















        # print([x for x in self.get_queryset()])

        # self.get_or_update_user(self.request.user)
        # self.create_order_items()

    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def get(self, request, *args, **kwargs):
    #     print(self.request.data, 'self.request.data')
    #     print(self.get_queryset(), 'self.queryset')
    #
    #     return super().create(request, *args, **kwargs)


class Splitter:
    """

    SPLIT

    """




# class OrderCreateAPIView(mixins.RetrieveModelMixin,
#                          mixins.ListModelMixin,
#                          mixins.CreateModelMixin,
#                          GenericAPIView):
#
#     serializer_class = OrderSerializer
#
#     def post(self, request, *args, **kwargs):
#         shopping_cart_items = self.get_serializer_context()['shopping_cart_items']
#         if not shopping_cart_items.exists():
#             return Response({'error': 'No items in shopping cart.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         super().create(request, *args, **kwargs)
#         # return redirect(reverse('orders-detail', kwargs={"pk": self.order_id}))
#         return redirect(reverse('orders-detail', kwargs={"pk": self.request.session['order_id']}))
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['user'] = self.request.user
#         context['shopping_cart_items'] = self.get_queryset()
#         return context
#
#     def perform_create(self, serializer):
#         """
#         Clear shopping cart after order is done.
#         """
#         order = serializer.save()
#         self.request.session['order_id'] = order.pk
#         # self.order_id = order.pk
#         shopping_cart_items = self.get_serializer_context()['shopping_cart_items']
#         shopping_cart_items.delete()
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset


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
