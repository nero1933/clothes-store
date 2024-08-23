from django.db.models.signals import post_save
from django.dispatch import receiver

from ecommerce.models.orders import Order
from ecommerce.models.payments import Payment


@receiver(post_save, sender=Order)
def create_payment(sender, instance, created, **kwargs):
    if created:
        Payment.objects.create(order=instance, stripe_session_id='')