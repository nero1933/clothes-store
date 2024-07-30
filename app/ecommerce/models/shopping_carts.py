import uuid

from django.db import models
from django.core.validators import MinValueValidator


class ShoppingCart(models.Model):
    user = models.OneToOneField('UserProfile', related_name='users', on_delete=models.CASCADE, null=True)
    # session_id = models.UUIDField(editable=False, unique=True, null=True)

    def __str__(self):
        return f"Shopping Cart for {self.user}"


class ShoppingCartItem(models.Model):
    cart = models.ForeignKey('ShoppingCart', related_name='shopping_cart_item', on_delete=models.CASCADE)
    product_variation = models.ForeignKey('ProductVariation', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
