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
            phone='+380951112233',
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

        response = self.client.post(reverse('token_obtain_pair'), data)
        return response.data.get('access')

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
        }

        address = Address.objects.create(**data)
        UserAddress.objects.create(address=address, user=user, is_default=is_default)

        return address

    # def create_shipping_method(self):
    #     self.shipping_method_1 = 1

    def create_discount(self, name='discount', discount_rate=10) -> Discount:
        # start_date = datetime(2023, 3, 27, 11, 2, 40, 742332, timezone.utc)
        # end_date = datetime(2023, 12, 31, 0, 0, 0, tzinfo=timezone.utc)

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

        :return: Products queryset
        """
        call_command('create_sizes_command')
        call_command('create_products_command')

        product_qs = Product.objects.all()

        return product_qs

    # def fill_shopping_cart(self, user, user_data, items=3):
    #     self.get_token(user_data)
    #     cart = ShoppingCart.objects.get(user=user)
    #
    #
    #     if items >= 1:
    #         ShoppingCartItem.objects.create(cart=cart,
    #                                         product_item_size_quantity=self.pisq_1,
    #                                         quantity=1,
    #                                         )
    #     if items >= 2:
    #         ShoppingCartItem.objects.create(cart=cart,
    #                                         product_item_size_quantity=self.pisq_2,
    #                                         quantity=1,
    #                                         )
    #     if items >= 3:
    #         ShoppingCartItem.objects.create(cart=cart,
    #                                         product_item_size_quantity=self.pisq_3,
    #                                         quantity=1,
    #                                         )
    #
    # def create_order(self, user_data):
    #     data = {
    #         "email": 'test1@test.com',
    #         "payment_method": 1,
    #         "shipping_address": {
    #             'name': 'r',
    #             'surname': 'n',
    #             'street': 'dm 15',
    #             'country': 'Ukraine',
    #             'region': 'ch',
    #             'city': 'ch',
    #             'post_code': 49000,
    #             'phone': '+380956663321',
    #         },
    #         "shipping_method": 1,
    #     }
    #
    #     response = self.get_response('POST', 'create_order', data=data, user_data=user_data, follow=True)
    #     order_id = response.data['id']
    #     order_item_id = [item['id'] for item in response.data['order_item']]
    #     return order_id, order_item_id
