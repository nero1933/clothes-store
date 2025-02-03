from django import forms
from django.contrib import admin

from ecommerce.models import Address
from ecommerce.models.orders import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    readonly_fields = ('pk', 'product_variation', 'quantity', 'item_price')
    exclude = ('price', )
    can_delete = False
    can_add_related = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return OrderItem.objects.select_related(
            'order__user',
            'product_variation__product_item__product',
            'product_variation__product_item__color',
            'product_variation__size',
        )

    def item_price(self, obj):
        if obj.price:
            return obj.price / 100

        return None


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = (
        'pk',
        'user',
        'guest',
        'price',
        'payment_method',
        'shipping_method',
        'order_address',
        'date_created',
    )
    exclude = ('shipping_address', 'order_price')
    search_fields = ('pk', 'user__email', 'shipping_address__phone_number', )
    inlines = [OrderItemInline]


    def get_queryset(self, request):
        return Order.objects.select_related(
            'user',
            'shipping_address',
        )

    def price(self, obj):
        if obj:
            return obj.order_price / 100

        return None


    def order_address(self, obj):
        if obj.shipping_address:
            return (
                f'First name: {obj.shipping_address.first_name}\n'
                f'Last name: {obj.shipping_address.last_name}\n'
                f'Street: {obj.shipping_address.street}\n'
                f'Unit number: {obj.shipping_address.unit_number}\n'
                f'City: {obj.shipping_address.city}\n'
                f'Post code: {obj.shipping_address.post_code}\n'
                f'Region: {obj.shipping_address.region}\n'
                f'Country: {obj.shipping_address.country}\n'
                f'Phone number: {obj.shipping_address.phone_number}\n'
            )

        return None












admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)