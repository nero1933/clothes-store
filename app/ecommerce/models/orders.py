from django.db import models
from django.core.validators import MinValueValidator

import enum

from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):

    class Meta:
        ordering = ('-date_created',)

    class OrderStatus(enum.Enum):
        NEW = 1
        PAYED = 2
        SHIPPED = 3
        DONE = 4
        RETURN = 5

    class OrderMethods(enum.Enum):
        CARD = 1
        CASH_ON_DELIVERY = 2
        BANK_TRANSFER = 3

    class ShippingMethods(enum.Enum):
        UPS = 1
        DHL = 2

    user = models.ForeignKey('UserProfile', on_delete=models.PROTECT, related_name='user_orders')
    guest = models.ForeignKey('UserProfile', on_delete=models.PROTECT, blank=True, null=True, related_name='guest_orders')
    email = models.EmailField(max_length=255, blank=False, null=False)
    phone = PhoneNumberField()
    payment_method = models.PositiveSmallIntegerField(choices=[(x.value, x.name) for x in OrderMethods], default=1)
    shipping_address = models.ForeignKey('Address', on_delete=models.PROTECT)
    shipping_method = models.PositiveSmallIntegerField(choices=[(x.value, x.name) for x in ShippingMethods], default=1)
    order_price = models.PositiveIntegerField()
    order_status = models.PositiveSmallIntegerField(choices=[(x.value, x.name) for x in OrderStatus], default=1)
    payment_link = models.URLField(max_length=255, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s order / {self.date_created}"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='order_item', on_delete=models.CASCADE)
    product_variation = models.ForeignKey('ProductVariation', related_name='order_item', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), ])
    price = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
