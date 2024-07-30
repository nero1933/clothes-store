from django.contrib import admin
from ecommerce.models.shopping_carts import ShoppingCart, ShoppingCartItem

admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)