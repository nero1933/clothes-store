from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.reverse import reverse

from ecommerce.models.addresses import Address, UserAddress
from ecommerce.models.orders import Order, OrderItem
from ecommerce.models.payments import Payment
from ecommerce.serializers.addresses import AddressSerializer
from ecommerce.serializers.products import ImageSerializer


class PaymentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('id', 'payment_bool', 'url')

    def get_url(self, obj):
        if not obj.payment_bool:
            return self.context['request'].build_absolute_uri(
                reverse('payment_checkout',
                        kwargs={'order_id': obj.order.id}))
        return None


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_code = serializers.SerializerMethodField()
    product_gender = serializers.SerializerMethodField()
    product_size = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()

    product_url = serializers.SerializerMethodField()
    review_url = serializers.SerializerMethodField()
    review_id = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product_variation', 'product_name', 'product_code', 'product_gender', 'product_size',
            'product_price', 'quantity', 'price', 'review_id', 'review_url', 'product_url', 'main_image'
        ]

    def get_product_name(self, obj):
        action = self.context.get('action')
        if action == 'retrieve':
            return obj.product_variation.product_item.product.name

    def get_product_code(self, obj):
        action = self.context.get('action')
        if action == 'retrieve':
            return obj.product_variation.product_item.product_code

    def get_product_gender(self, obj):
        action = self.context.get('action')
        if action == 'retrieve':
            return obj.product_variation.product_item.product.gender

    def get_product_size(self, obj):
        action = self.context.get('action')
        if action == 'retrieve':
            return obj.product_variation.size.name

    def get_product_price(self, obj):
        action = self.context.get('action')
        if action == 'retrieve':
            return obj.product_variation.product_item.price

    def get_review_id(self, obj):
        action = self.context.get('action')
        if action == 'retrieve':
            try:
                return obj.review.pk
            except ObjectDoesNotExist:
                return None

    def get_review_url(self, obj):
        action = self.context.get('action')
        if action == 'retrieve' and obj.order.payment.payment_bool:
            return self.context['request'].build_absolute_uri(
                reverse('reviews_create',
                        kwargs={'order_id': obj.order.id,
                                'order_item_id': obj.pk,
                                'product_slug': obj.product_variation.product_item.product.slug}))

        return None

    def get_product_url(self, obj):
        action = self.context.get('action')
        if action == 'retrieve':
            return self.context['request'].build_absolute_uri(
                reverse('products-detail',
                        kwargs={'slug': obj.product_variation.product_item.product.slug}))

        return None

    def get_main_image(self, obj):
        action = self.context.get('action')
        if action == 'retrieve':
            # Access the prefetch related images
            main_image = None
            for image in obj.product_variation.product_item.image.all():
                if image.is_main:
                    main_image = image
                    break
            if main_image:
                return ImageSerializer(main_image).data

            # or just return qs[0]

        return None


class OrderDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    order_item = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user_id', 'email', 'payment', 'order_price', 'order_item')


class OrderListSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'order_price', 'order_status', 'payment', 'date_created')


class OrderCreateSerializer(serializers.ModelSerializer):
    order_price = serializers.IntegerField(read_only=True)
    shipping_method = serializers.ChoiceField(choices=[(x.value, x.name) for x in Order.ShippingMethods])
    payment_method = serializers.ChoiceField(choices=[(x.value, x.name) for x in Order.OrderMethods])
    payment = PaymentSerializer(read_only=True)


class OrderUserCreateSerializer(OrderCreateSerializer):
    """
    User have to choose shipping address from existing ones
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    shipping_address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.none())

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'shipping_address', 'shipping_method',
            'payment_method', 'order_price', 'payment',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            self.fields['shipping_address'].queryset = (
                Address.objects \
                    .prefetch_related('address__user')
                    .filter(address__user=request.user))

    def create(self, validated_data):
        order_price = self.context.get('order_price', None)
        order = Order.objects.create(order_price=order_price, **validated_data)
        order.save()
        return order


class OrderGuestCreateSerializer(OrderCreateSerializer):
    """
    Guest have to enter new shipping address
    """
    email = serializers.EmailField(write_only=True)
    shipping_address = AddressSerializer()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    guest = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'guest', 'shipping_address', 'shipping_method',
            'payment_method', 'order_price', 'payment', 'email'
        ]


    def create(self, validated_data):
        validated_data.pop('email', None)

        user = self.context.get('user', None)
        guest = self.context.get('guest', None)
        order_price = self.context.get('order_price', None)

        shipping_address_data = validated_data.pop('shipping_address')
        shipping_address = Address.objects.create(**shipping_address_data)

        UserAddress.objects.create(address=shipping_address, user=user)

        order = Order.objects.create(
            shipping_address=shipping_address,
            order_price=order_price,
            user=user,
            guest=guest,
            **validated_data
        )

        order.save()

        return order
