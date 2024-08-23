import stripe

from django.core.management.base import BaseCommand

from app import settings

from ecommerce.models import ProductItem


stripe.api_key = settings.STRIPE_SECRET_KEY


class Command(BaseCommand):
    help = 'Creates sizes for developing and testing purposes.'

    def handle(self, *args, **options):
        product_items_qs = ProductItem.objects.select_related('product').all()
        for product_item in product_items_qs:
            stripe_product = stripe.Product.create(
                name=product_item.product.name,
                description=product_item.product.description,
            )
            stripe_price = stripe.Price.create(
                product=stripe_product.id,
                unit_amount=product_item.price,
                currency='eur',
            )
            product_item.stripe_product_id = stripe_product.id
            product_item.stripe_price_id = stripe_price.id
            product_item.save()
