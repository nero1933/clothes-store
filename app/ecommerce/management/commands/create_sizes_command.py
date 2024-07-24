from django.core.management.base import BaseCommand

from ecommerce.models import SizeCategory, ProductSize
from ecommerce.utils.products import sizes


class Command(BaseCommand):
    help = 'Creates sizes for developing and testing purposes.'

    def handle(self, *args, **options):

        def _create_size_categories():
            objs = (SizeCategory(name=cat_name) for cat_name in sizes.size_categories)
            SizeCategory.objects.bulk_create(objs)

        def _create_product_sizes():
            size_cat_queryset = SizeCategory.objects.all()
            bulk_list = []
            for size_cat, size_names in sizes.sizes.items():
                size_cat_obj = size_cat_queryset.get(name=size_cat)
                for size_name in size_names:
                    bulk_list.append(ProductSize(
                        name=size_name[0],
                        size_category=size_cat_obj,
                    ))

            ProductSize.objects.bulk_create(bulk_list)

        try:
            _create_size_categories()
            _create_product_sizes()
            self.stdout.write(self.style.SUCCESS(f'All sizes are successfully created'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
