from phonenumber_field.serializerfields import PhoneNumberField

from rest_framework import serializers
from rest_framework.reverse import reverse

from ecommerce.models.addresses import Address, UserAddress
from ecommerce.models.orders import Order, OrderItem
from ecommerce.models.payments import Payment
from ecommerce.serializers.addresses import AddressSerializer


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variation', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    order_price = serializers.IntegerField(read_only=True)
    shipping_method = serializers.ChoiceField(choices=[(x.value, x.name) for x in Order.ShippingMethods])
    payment_method = serializers.ChoiceField(choices=[(x.value, x.name) for x in Order.OrderMethods])
    payment_link = serializers.SerializerMethodField()

    def get_payment_link(self, obj):
        if obj:
            # Use the reverse function to generate the URL dynamically
            return self.context['request'].build_absolute_uri(
                reverse('payment_checkout', kwargs={'order_id': obj.id})
            )

        return None


class OrderUserCreateSerializer(OrderCreateSerializer):
    """
    User have to choose shipping address from existing ones
    """
    email = serializers.EmailField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # guest = serializers.PrimaryKeyRelatedField(default=None, allow_null=True, read_only=True)
    shipping_address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.none())

    class Meta:
        model = Order
        fields = ['id', 'user', 'email', 'shipping_address', 'shipping_method',
                  'payment_method', 'order_price', 'payment_link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            self.fields['shipping_address'].queryset = (
                Address.objects \
                    .prefetch_related('address__user')
                    .filter(address__user=request.user))

    def create(self, validated_data):
        user = self.context.get('user', None)
        order_price = self.context.get('order_price', None)
        order = Order.objects.create(email=user.email, order_price=order_price, **validated_data)
        order.payment_link = self.get_payment_link(order)
        order.save()
        return order


class OrderGuestCreateSerializer(OrderCreateSerializer):
    """
    Guest have to enter new shipping address
    """
    email = serializers.EmailField()
    phone = PhoneNumberField()
    shipping_address = AddressSerializer()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    guest = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'email', 'user', 'guest', 'phone', 'shipping_address', 'shipping_method',
                  'payment_method', 'order_price', 'payment_link', ]


    def create(self, validated_data):
        user = self.context.get('user', None)
        guest = self.context.get('guest', None)
        order_price = self.context.get('order_price', None)

        shipping_address_data = validated_data.pop('shipping_address')
        shipping_address = Address.objects.create(**shipping_address_data)

        UserAddress.objects.create(address=shipping_address, user=user)

        order = Order.objects.create(
            shipping_address=shipping_address,
            order_price=order_price,user=user,
            guest=guest,**validated_data
        )

        order.payment_link = self.get_payment_link(order)
        order.save()

        return order
