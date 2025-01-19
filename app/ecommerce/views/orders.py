from abc import abstractmethod

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from app import settings
from ecommerce.models import UserProfile, Payment, Review, Product, ProductItem, ProductVariation, Image, Address
from ecommerce.models.orders import Order, OrderItem
from ecommerce.models.shopping_carts import ShoppingCartItem
from ecommerce.serializers.orders import OrderGuestCreateSerializer, OrderUserCreateSerializer, OrderListSerializer, \
    OrderDetailSerializer


class OrderViewSet(ReadOnlyModelViewSet):
    # serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Order.objects \
            .prefetch_related('payment') \
            .filter(user=self.request.user)

        return queryset

    def get_object(self):
        payment_queryset = Payment.objects.only('id', 'order_id', 'payment_bool')  # Only fetch necessary fields
        review_queryset = Review.objects.only('id', 'order_item_id', )
        product_variation_queryset = ProductVariation.objects.only('id', 'product_item_id')
        product_item_queryset = ProductItem.objects.only('id', 'product_id')
        product_queryset = Product.objects.only('id', 'slug')
        image_queryset = Image.objects.filter(is_main=True)

        obj = Order.objects \
            .prefetch_related(
                Prefetch('order_item__review', queryset=review_queryset),
                Prefetch('payment', queryset=payment_queryset),
                Prefetch('order_item__product_variation', queryset=product_variation_queryset),
                Prefetch('order_item__product_variation__product_item', queryset=product_item_queryset),
                Prefetch('order_item__product_variation__product_item__image', queryset=image_queryset),
                Prefetch('order_item__product_variation__product_item__product', queryset=product_queryset)
            ) \
            .defer('guest') \
            .get(user=self.request.user, pk=self.kwargs['pk'])

        return obj

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action  # Pass the current action to the context
        return context

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        elif self.action == 'list':
            return OrderListSerializer

class OrderCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ShoppingCartItem.objects \
            .select_related('cart__user',
                            'product_variation',
                            'product_variation__product_item') \
            .prefetch_related('product_variation__product_item__discount') \
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

    def set_user_in_context(self, serializer):
        serializer.context['user'] = self.request.user

    def transform_guest_to_user(self, serializer):
        pass

    def create(self, request, *args, **kwargs):
        """
        Test
        """
        # user = request.user
        serializer = self.get_serializer(data=request.data)

        order_items = self.prepare_order_items()

        if not order_items:
            return Response("Can't create the order because the shopping cart is empty", status=status.HTTP_400_BAD_REQUEST)

        order_price = sum(map(lambda x: x.price, order_items))
        serializer.context['order_price'] = order_price

        self.set_user_in_context(serializer)

        # user_exists = self.get_user(request.data.get('email', None))
        # if user.is_guest and user_exists: # if existing user makes order from guest account
        #     # existing account assigned to order (to let user see his new order in account)
        #     serializer.context['user'] = user_exists
        #     # guest_user assigned to guest (to let logged in guest make a payment)
        #     serializer.context['guest'] = user
        # else:
        #     serializer.context['user'] = user

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        order_id = serializer.data['id']
        self.create_order_items(order_id, order_items)

        self.empty_shopping_cart()

        self.transform_guest_to_user(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderUserCreateAPIView(OrderCreateAPIView):
    serializer_class = OrderUserCreateSerializer


class OrderGuestCreateAPIView(OrderCreateAPIView):
    serializer_class = OrderGuestCreateSerializer

    def set_user_form_email(self, email: str):
        """
        Try to find the user with the given email address.
        Set 'self.user_form_email' to UserProfile if there is such user.
        If there is no user set None.
        """

        try:
            self.user_form_email = UserProfile.objects.get(email=email)
        except ObjectDoesNotExist:
            self.user_form_email = None

    # def guest_to_user(self, user, user_data):
    #     new_email = user_data['email']
    #     new_phone = user_data['phone']
    #     first_name = user_data['shipping_address']['first_name']
    #     last_name = user_data['shipping_address']['last_name']
    #     user = UserProfile.guest_to_user(user, new_email, first_name, last_name, new_phone)
    #     return user

    def set_user_in_context(self, serializer):
        # Set 'self.user_form_email' to user object whose email was entered in the order
        self.set_user_form_email(self.request.data.get('email', None))

        if self.request.user.is_guest and self.user_form_email: # if existing user makes order from guest account
            # existing account assigned to order (to let user see his new order in account)
            serializer.context['user'] = self.user_form_email
            # guest_user assigned to guest (to let already logged in guest make a payment)
            serializer.context['guest'] = self.request.user
        else:
            # if it is first order from a new user
            serializer.context['user'] = self.request.user

    def transform_guest_to_user(self, serializer):
        if self.request.user:
            return None

        user = self.request.user

        if user.is_guest:
            self.guest_to_user(user, serializer.validated_data)

            new_email = serializer.validated_data['email']
            first_name = serializer.validated_data['shipping_address']['first_name']
            last_name = serializer.validated_data['shipping_address']['last_name']
            user = UserProfile.guest_to_user(user, new_email, first_name, last_name)



    #     response = super().post(request, *args, **kwargs)
    #
    #     if response.status_code == status.HTTP_201_CREATED:
    #         user = self.get_user(request.data.get('email', None))
    #         if user:
    #             return response
    #
    #         user = self.request.user
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #
    #         if user.is_guest:
    #             self.guest_to_user(user, serializer.validated_data)
    #
    #     return response
