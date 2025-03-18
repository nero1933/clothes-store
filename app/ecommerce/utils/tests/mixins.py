from datetime import datetime
from urllib.parse import urlparse

from django.core.management import call_command
from django.db.models import QuerySet

from rest_framework.test import APITestCase

from ecommerce.models import *


class TestAPIEcommerce(APITestCase):

    default_email = 'test@test.com'
    password = '12345678'
    user = None
    jwt_access_token = None

    def create_user(self, email=default_email) -> UserProfile:
        """
        Creates test user

        :param email: users email
        :return: UserProfile object
        """
        user = UserProfile.objects.create_user(
            email=email,
            first_name='test',
            last_name='test',
            password=self.password
        )

        user.is_active = True
        user.save()

        return user

    def get_jwt_access_token(self, email=default_email) -> str:
        """
        logs in user

        :param email: users email
        :return: JWT access token
        """
        data = {'email': email, 'password': self.password}

        response = self.client.post(reverse('login'), data)
        return response.data.get('access_token')

    def create_address(self, user, is_default) -> Address:
        """
        Creates address for user

        :param user: users email
        :param is_default: is default address
        :return: Address object
        """
        data = {
            'first_name': 'Name',
            'last_name': 'Surname',
            'street': 'st',
            'unit_number': '1',
            'country': 'Ukraine',
            'region': 'Kyivskaya oblast',
            'city': 'Kyiv',
            'post_code': 55000,
            'phone_number': '+380993332211'
        }

        address = Address.objects.create(**data)
        UserAddress.objects.create(address=address, user=user, is_default=is_default)

        return address

    def create_discount(self, name='discount', discount_rate=10) -> Discount:

        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)

        discount = Discount.objects.create(
            name=name,
            description='discount',
            discount_rate=discount_rate,
            start_date=start_date,
            end_date=end_date
        )

        return discount

    def create_products(self) -> QuerySet:
        """
        Creates products

        :return: ProductItem queryset
        """
        call_command('create_sizes_command', silence=True)
        call_command('create_products_command', silence=True)

        product_qs = Product.objects.all()

        return product_qs

    def create_image(self, product_item) -> Image:
        url = 'https://{domain}.com'
        domain = uuid.uuid4().hex

        image = Image.objects.create(
            product_item=product_item,
            name='image',
            url=url.format(domain=domain),
            is_main=True,
        )

        return image


class TestAPIOrder(TestAPIEcommerce):

    def setUp(self):
        call_command('create_sizes_command', silence=True)
        call_command('create_products_command', silence=True)

        self.user = self.create_user()
        self.jwt_access_token = self.get_jwt_access_token()
        self.address = self.create_address(self.user, is_default=False)
        self.email = 'email@email.email'
        self.address_dict = {
            'first_name': 'test',
            'last_name': 'test',
            'street': 'test',
            'unit_number': '1',
            'country': 'Ukraine',
            'region': 'Kyivskaya oblast',
            'city': 'Kyiv',
            'post_code': '55000',
            'phone_number': '+380993332211'
        }
        self.shipping_method = 1
        self.payment_method = 1
        self.order_data_guest = {
            'email': self.email,
            'shipping_address': self.address_dict,
            'shipping_method': self.shipping_method,
            'payment_method': self.payment_method,
        }

        self.product_variation_1 = ProductVariation.objects \
            .select_related('product_item') \
            .prefetch_related('product_item__discount') \
            .first()
        self.product_variation_2 = ProductVariation.objects \
            .select_related('product_item') \
            .prefetch_related('product_item__discount') \
            .last()

        self.create_image(self.product_variation_1.product_item)
        # self.create_image(self.product_variation_2.product_item) # leave 2-nd product item without main image

        discount_1 = self.create_discount(name='discount 1', discount_rate=10)
        discount_2 = self.create_discount(name='discount 2', discount_rate=20)

        self.product_variation_1.product_item.discount.set([discount_1, discount_2])
        product_variation_1_discount_price = self.product_variation_1.product_item.get_discount_price()

        self.product_data_1 = {
            'product_variation': self.product_variation_1.pk,
            'quantity': 3 if self.product_variation_1.qty_in_stock >= 3 else self.product_variation_1.qty_in_stock
        }

        self.product_data_2 = {
            'product_variation': self.product_variation_2.pk,
            'quantity': 2 if self.product_variation_2.qty_in_stock >= 2 else self.product_variation_2.qty_in_stock
        }

        product_variation_1_order_item_price = (
                product_variation_1_discount_price * self.product_data_1.get('quantity'))
        product_variation_2_order_item_price = (
                self.product_variation_2.product_item.get_discount_price() * self.product_data_2.get('quantity'))
        self.order_price = product_variation_1_order_item_price + product_variation_2_order_item_price

        self.url_shopping_cart = 'shopping_cart_items-list'
        self.url_order_user = 'create_order_user'
        self.url_order_guest = 'create_order_guest'
        self.url_order_list = 'orders-list'
        self.url_order_detail = 'orders-detail'
        self.url_register_guest = 'register_guest'
        self.url_token = 'login'

    def login_as_user(self):
        data = {'email': self.email, 'password': '123456789'}

        response = self.client.post(reverse(self.url_token), data)
        self.assertEqual(response.status_code, 200, 'User must be able to log in')

        user_jwt = response.data.get('access_token')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_jwt)

    def log_in_as_guest(self):
        response = self.client.post(reverse(self.url_register_guest), format='json')
        self.assertEqual(response.status_code, 201, 'Guest user must be register')

        jwt = response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)

    def fill_in_shopping_cart(self):
        response = self.client.post(reverse(self.url_shopping_cart), self.product_data_1, format='json')
        self.assertEqual(response.status_code, 201, 'Shopping cart items must be created successfully')
        response = self.client.post(reverse(self.url_shopping_cart), self.product_data_2, format='json')
        self.assertEqual(response.status_code, 201, 'Shopping cart items must be created successfully')

    def create_guest_order(self):
        self.log_in_as_guest()
        self.fill_in_shopping_cart()

        response = self.client.post(reverse(self.url_order_guest), self.order_data_guest, format='json')
        return response

    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
