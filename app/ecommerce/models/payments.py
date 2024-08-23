from django.db import models


class Payment(models.Model):
    order = models.OneToOneField('Order', related_name='payment', on_delete=models.CASCADE)
    # user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_session_id = models.CharField(max_length=500, blank=True)
