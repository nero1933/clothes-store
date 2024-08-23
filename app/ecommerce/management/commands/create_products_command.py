import uuid
import random

import stripe

from app import settings

from django.core.management.base import BaseCommand

from ecommerce.models import Brand, Color, AttributeType, SizeCategory, ProductCategory, Product, ProductItem, \
    ProductVariation, ProductSize, AttributeOption

from slugify import slugify

from ecommerce.utils.products.sizes import sizes




class Command(BaseCommand):
    help = 'Creates products for developing ang testing purposes.'

    def handle(self, *args, **options):

        def get_sizes() -> dict:
            size_dict = {}
            size_cat_qs = SizeCategory.objects.all()
            for size_cat in size_cat_qs:
                if size_cat.name == 'SHOES':
                    size_dict['size_shoes'] = size_cat
                elif size_cat.name == 'CLOTHES':
                    size_dict['size_clothes'] = size_cat
                elif size_cat.name == 'BAGS':
                    size_dict['size_bags'] = size_cat

            return size_dict

        def get_cats() -> dict:
            cat_dict = {}
            cat_qs = ProductCategory.objects.all()
            for cat in cat_qs:
                if cat.name == 't-shirt':
                    cat_dict['cat_t_shirt'] = cat
                elif cat.name == 'hoodie':
                    cat_dict['cat_hoodie'] = cat
                elif cat.name == 'trousers':
                    cat_dict['cat_trousers'] = cat
                elif cat.name == 'hat':
                    cat_dict['cat_hat'] = cat
                elif cat.name == 'backpack':
                    cat_dict['cat_backpack'] = cat
                elif cat.name == 'shoes':
                    cat_dict['cat_shoes'] = cat
                elif cat.name == 'sneakers':
                    cat_dict['cat_sneakers'] = cat
                elif cat.name == 'flip_flops':
                    cat_dict['cat_flip_flops'] = cat

            return cat_dict

        def get_attr_options() -> dict:
            attr_options_dict = {
                'fit': ['normal', 'oversize', 'slim'],
                'season': ['spring/autumn', 'summer', 'winter'],
                'style': ['casual', 'sport', 'classic']
            }

            return attr_options_dict


        def _create_simplemodel(model, lst):
            objs = (model(name=name, slug=slugify(name)) for name in lst)
            model.objects.bulk_create(objs)

        def _create_brands():
            brands = ['nike', 'puma', 'adidas', 'new_balance', 'reebok', 'asics', 'north_sails']
            _create_simplemodel(Brand, brands)

        def _create_colors():
            colors = ['red', 'orange', 'yellow', 'green', 'blue', 'violet']
            _create_simplemodel(Color, colors)

        def _create_attribute_types():
            attribute_types = ['fit', 'season', 'style']
            _create_simplemodel(AttributeType, attribute_types)

        def _create_attribute_options():
            bulk_list = []
            attr_options_dict = get_attr_options()
            attr_types_qs =  AttributeType.objects.all()

            for obj in attr_types_qs:
                for option in attr_options_dict[obj.name]:
                    bulk_list.append(AttributeOption(attribute_type=obj, name=option))

            AttributeOption.objects.bulk_create(bulk_list)

        def _create_categories():
            size_dict = get_sizes()

            name = ['t-shirt', 'hoodie', 'trousers', 'hat', 'backpack', 'shoes', 'sneakers', 'flip_flops']
            desc = 'desc'

            bulk_list = [
                ProductCategory(name=name[0], slug=slugify(name[0]), description=desc, size_category=size_dict['size_clothes']),
                ProductCategory(name=name[1], slug=slugify(name[1]), description=desc, size_category=size_dict['size_clothes']),
                ProductCategory(name=name[2], slug=slugify(name[2]), description=desc, size_category=size_dict['size_clothes']),
                ProductCategory(name=name[3], slug=slugify(name[3]), description=desc, size_category=size_dict['size_clothes']),
                ProductCategory(name=name[4], slug=slugify(name[4]), description=desc, size_category=size_dict['size_bags']),
            ]

            parent_category_shoes = ProductCategory(name=name[5], slug=slugify(name[5]),
                                                    description=desc, size_category=size_dict['size_shoes'])

            bulk_list.append(parent_category_shoes)

            ProductCategory.objects.bulk_create(bulk_list)

            bulk_list = [
                ProductCategory(name=name[6], slug=slugify(name[6]),
                                description=desc, size_category=size_dict['size_shoes'],
                                parent_category=parent_category_shoes),
                ProductCategory(name=name[7], slug=slugify(name[7]),
                                description=desc, size_category=size_dict['size_shoes'],
                                parent_category=parent_category_shoes),
            ]

            ProductCategory.objects.bulk_create(bulk_list)


        def _create_products():
            names = ['simple t-shirt', 'oversize hoodie', 'new trousers', 'summer hat',
                     'small backpack', 'running sneakers', 'beach flip flops']
            decs = 'decs'
            genders = ['M', 'W']
            cat_dict = get_cats()
            attr_options_dict = get_attr_options()

            brand_qs = Brand.objects.all()
            attr_options_qs = AttributeOption.objects.all()

            for attr_option in attr_options_qs:
                for k, v in attr_options_dict.items():
                    if attr_option.name in v:
                        attr_options_dict[k].append(attr_option)
                        attr_options_dict[k].remove(attr_option.name)

            bulk_list = [
                Product(name=names[0], slug=slugify(names[0]), description=decs,
                        gender=genders[0], category=cat_dict['cat_t_shirt']),
                Product(name=names[1], slug=slugify(names[1]), description=decs,
                        gender=genders[0], category=cat_dict['cat_hoodie']),
                Product(name=names[2], slug=slugify(names[2]), description=decs,
                        gender=genders[0], category=cat_dict['cat_trousers']),
                Product(name=names[3], slug=slugify(names[3]), description=decs,
                        gender=genders[1], category=cat_dict['cat_hat']),
                Product(name=names[4], slug=slugify(names[4]), description=decs,
                        gender=genders[1], category=cat_dict['cat_backpack']),
                Product(name=names[5], slug=slugify(names[5]), description=decs,
                        gender=genders[1], category=cat_dict['cat_sneakers']),
                Product(name=names[6], slug=slugify(names[6]), description=decs,
                        gender=genders[1], category=cat_dict['cat_flip_flops']),
            ]

            for product in bulk_list:
                product.brand = brand_qs[random.randint(0, len(brand_qs) - 1)]

            Product.objects.bulk_create(bulk_list)
            obj_list = Product.objects.all()

            for product in obj_list:
                selected_options = []
                for k, v in attr_options_dict.items():
                    selected_options.append(random.choice(v))

                product.attribute_option.set(selected_options)
                product.save()

        def _create_product_items():

            bulk_list = []
            price_range = (3900, 11900)

            product_qs = Product.objects.all()
            color_qs = Color.objects.all()

            for product in product_qs:
                obj = ProductItem(
                    product=product,
                    color=random.choice(color_qs),
                    price=random.randint(price_range[0], price_range[1]),
                    product_code=uuid.uuid4().hex,
                )

                bulk_list.append(obj)

                obj_2 = ProductItem(
                    product=obj.product,
                    color=random.choice([color for color in color_qs if color != obj.color]),
                    price=obj.price,
                    product_code=uuid.uuid4().hex,
                )

                bulk_list.append(obj_2)

            ProductItem.objects.bulk_create(bulk_list)

        def _create_product_variations():
            bulk_list = []
            qty_range = (1, 100)

            product_items_qs = ProductItem.objects.all().select_related(
                'product',
                'product__category',
                'product__category__size_category'
            )
            size_qs = ProductSize.objects.all()

            for p in product_items_qs:
                random_size = random.choice(sizes[p.product.category.size_category.name])
                prod_size = [x for x in size_qs if x.name == random_size[0]][0]

                obj = ProductVariation(
                    product_item=p,
                    size=prod_size,
                    qty_in_stock=random.randint(*qty_range),
                )
                bulk_list.append(obj)

            ProductVariation.objects.bulk_create(bulk_list)


        try:
            _create_brands()
            _create_colors()
            _create_attribute_types()

            _create_attribute_options()

            _create_categories()

            _create_products()

            _create_product_items()

            _create_product_variations()

            self.stdout.write(self.style.SUCCESS(f'All products are successfully created'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))