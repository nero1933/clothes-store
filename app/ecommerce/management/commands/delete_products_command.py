from django.core.management import BaseCommand
from sendgrid import Category

from ecommerce.models import Product, Brand, Color, ProductCategory, ProductItem, AttributeType


class Command(BaseCommand):
    help = 'Creates products for developing ang testing purposes.'

    def handle(self, *args, **options):
        try:
            Brand.objects.all().delete()
            Color.objects.all().delete()
            AttributeType.objects.all().delete()
            ProductCategory.objects.all().delete()
            Product.objects.all().delete()
            ProductItem.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'All products are successfully deleted'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
