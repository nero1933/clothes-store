from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from ecommerce.models import UserProfile, Product, OrderItem


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='review')
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='review')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    comment = models.TextField(max_length=255, blank=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.user}, Product: {self.order_item.product_variation.product_item.product.name}, Rating: {self.rating}'
