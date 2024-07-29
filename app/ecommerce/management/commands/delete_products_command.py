from django.core.management import BaseCommand

from ecommerce.models import Product, Brand, Color, ProductCategory, ProductItem, AttributeType, AttributeOption, \
    ProductVariation


class Command(BaseCommand):
    help = 'Creates products for developing ang testing purposes.'

    def handle(self, *args, **options):
        models = [Product, Brand, Color, ProductCategory, ProductItem, ProductVariation, AttributeType, AttributeOption]

        try:
            for model in models:
                model.objects.all().delete()

            self.stdout.write(self.style.SUCCESS(f'All products are successfully deleted'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
