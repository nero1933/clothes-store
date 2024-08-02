from django.contrib import admin
from ecommerce.models.orders import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)