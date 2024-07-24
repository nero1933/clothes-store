from django.core.management.base import BaseCommand

from ecommerce.models import SizeCategory, ProductSize


class Command(BaseCommand):
    help = 'Creates products. Used in developing and testing.'

    def handle(self, *args, **options):

        def _create_size_categories():
            self.size_cat_clothes = SizeCategory.objects.create(name='clothes')
            self.size_cat_shoes = SizeCategory.objects.create(name='shoes')

        def _create_product_sizes():
            ProductSize.objects.create(name='S', size_categories=self.size_cat_clothes)
            ProductSize.objects.create(name='M', size_categories=self.size_cat_clothes)
            ProductSize.objects.create(name='L', size_categories=self.size_cat_clothes)

        _create_size_categories()
        _create_product_sizes()