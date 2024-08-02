import secrets
import string

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from ..models.addresses import Address, UserAddress
from ..models.users import UserProfile
from ..models.orders import Order, OrderItem
from ..serializers.addresses import  AddressSerializer


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product_item_size_quantity', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    order_item = OrderItemSerializer(many=True, read_only=True)
    order_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    shipping_address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['id', 'user', 'email', 'shipping_address', 'shipping_method', 'payment_method', 'order_item', 'order_price']

    def create(self, validated_data):
        # User can be ether user or guest. If he is guest than
        # create user profile based on information from order.
        user = self.get_or_create_user(validated_data)

        shipping_address = self.get_address(validated_data, user)
        validated_data.pop('shipping_address')

        # Every item from shopping cart recreates to order items,
        # after what calculates price for all order and order creates.
        order = self.cart_to_order(validated_data, user, shipping_address)
        return order

    def get_or_create_user(self, validated_data):
        # !
        # CHANGE FROM UNAUTH TO USER -> TO -> FROM GUEST TO USER
        # !
        if self.context['request'].user.is_authenticated:
            user = self.context['request'].user
        else:
            # Get all required information to create a new user
            vd = validated_data.copy()
            shipping_address = vd.pop('shipping_address')

            email = vd.pop('email')
            try:
                user = UserProfile.objects.get(email=email)
            except ObjectDoesNotExist:
                name = shipping_address.pop('name')
                phone = shipping_address.pop('phone')

                chars = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(chars) for _ in range(8))

                user = UserProfile.objects.create_user(email=email, name=name, phone=phone, password=password)

        return user

    def get_address(self, validated_data, user):
        vd = validated_data.copy()
        shipping_address_data = vd.pop('shipping_address')
        shipping_address = Address.objects.create(**shipping_address_data)

        UserAddress.objects.create(address=shipping_address, user=user)
        return shipping_address

    def cart_to_order(self, validated_data, user, shipping_address):
        order_items = []
        for item in self.context['shopping_cart_items']:
            order_items.append(
                OrderItem(product_item_size_quantity=item.product_item_size_quantity,
                          quantity=item.quantity,
                          price=item.product_item_size_quantity.product_item.get_price() * item.quantity,
                          )
            )

        order_price = sum(item.price for item in order_items)

        #validated_data.pop('shipping_address')
        order = Order.objects.create(user=user,
                                     shipping_address=shipping_address,
                                     order_price=order_price,
                                     **validated_data)

        for item in order_items:
            item.order = order

        OrderItem.objects.bulk_create(order_items)
        return order
