import stripe

from django.db.models.signals import post_save
from django.dispatch import receiver

from app import settings

from ecommerce.models import ProductItem

stripe.api_key = settings.STRIPE_SECRET_KEY

@receiver(post_save, sender=ProductItem)
def update_stripe_price(sender, instance, created, **kwargs):
    """ Update stripe's price if ProductItem's price was changed """
    if not created and instance.stripe_price_id:
        if not hasattr(instance, '_prevent_signal_loop'):
            # Set the flag to prevent the signal from looping
            instance._prevent_signal_loop = True
            # Update the existing stripe.Price object
            stripe.Price.modify(
                instance.stripe_price_id,
                active=False,
            )
            # Create new stripe.Price instance
            stripe_price = stripe.Price.create(
                product=instance.stripe_product_id,
                currency="eur",
                unit_amount=instance.price,
            )
            # Set new 'stripe_price_id' to ProductItem instance
            instance.stripe_price_id = stripe_price.id
            instance.save()