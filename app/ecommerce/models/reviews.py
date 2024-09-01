from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from ecommerce.models import UserProfile, Product, OrderItem


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(max_length=255, blank=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'User: {self.user}, Product: {self.product}, Rating: {self.rating}'
