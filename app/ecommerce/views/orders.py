from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer, OpenApiParameter, \
    PolymorphicProxySerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ecommerce.models import UserProfile
from ecommerce.models.orders import Order, OrderItem
from ecommerce.models.shopping_carts import ShoppingCartItem
from ecommerce.serializers.addresses import AddressSerializer
from ecommerce.serializers.orders import OrderGuestCreateSerializer, OrderUserCreateSerializer, OrderSerializer


class OrderViewSet(ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects \
            .prefetch_related('order_item',
                              'payment') \
            .filter(user=self.request.user)

        return queryset

class OrderCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ShoppingCartItem.objects \
            .select_related('cart__user',
                            'product_variation',
                            'product_variation__product_item') \
            .prefetch_related('cart__user__address',
                              'product_variation__product_item__discount') \
            .filter(cart__user=self.request.user)

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

    def create_order_items(self, order_id: int, bulk_list: list[OrderItem]):
        for item in bulk_list:
            item.order_id = order_id

        OrderItem.objects.bulk_create(bulk_list)

    def empty_shopping_cart(self):
        queryset = self.get_queryset()
        queryset.delete()

    def get_user(self):
        try:
            user = UserProfile.objects.get(email=self.request.data.get('email', None))
            return user
        except ObjectDoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        """
        Test
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)

        order_items = self.prepare_order_items()

        if not order_items:
            return Response("Can't create the order because the shopping cart is empty", status=status.HTTP_400_BAD_REQUEST)

        order_price = sum(map(lambda x: x.price, order_items))
        serializer.context['order_price'] = order_price

        user_exists = self.get_user()
        if user.is_guest and user_exists: # if existing user makes order from guest account
            serializer.context['user'] = user_exists # existing account assigned to order
            user.delete() # guest user is deleted
        else:
            serializer.context['user'] = user

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        order_id = serializer.data['id']
        self.create_order_items(order_id, order_items)

        self.empty_shopping_cart()

        # SEND EMAIL WITH ORDER DETAIL TO THE USER
        #
        # WRITE HERE

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderUserCreateAPIView(OrderCreateAPIView):
    serializer_class = OrderUserCreateSerializer


class OrderGuestCreateAPIView(OrderCreateAPIView):
    serializer_class = OrderGuestCreateSerializer

    def guest_to_user(self, user, user_data):
        new_email = user_data['email']
        new_phone = user_data['phone']
        first_name = user_data['shipping_address']['first_name']
        last_name = user_data['shipping_address']['last_name']
        user = UserProfile.guest_to_user(user, new_email, first_name, last_name, new_phone)
        return user

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            user = self.get_user()
            if user:
                return response

            user = self.request.user
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if user.is_guest:
                self.guest_to_user(user, serializer.validated_data)

        return response





















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
