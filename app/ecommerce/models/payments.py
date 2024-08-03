from django.db import models
from rest_framework.authtoken.admin import User


class Payment(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)
