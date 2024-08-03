from django.db.models.signals import post_save
from django.dispatch import receiver

from ecommerce.models import UserProfile, ShoppingCart


@receiver(post_save, sender=UserProfile)
def create_user_shopping_cart(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(user=instance)