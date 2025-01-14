from rest_framework.reverse import reverse

from ecommerce.models import UserProfile, Address
from ecommerce.utils.tests.mixins import TestAPIOrder


class TestOrders(TestAPIOrder):

    def setUp(self):
        super().setUp()
    #     super().setUp()
    #     self.create_products()
    #
    #     self.user = self.create_user()
    #     self.jwt_access_token = self.get_jwt_access_token()
    #     self.address = self.create_address(self.user, is_default=False)
    #     self.email = 'email@email.email'
    #     self.phone = '+380985552288'
    #     self.address_dict = {
    #         'first_name': 'test',
    #         'last_name': 'test',
    #         'street': 'test',
    #         'unit_number': '1',
    #         'country': 'Ukraine',
    #         'region': 'Kyivskaya oblast',
    #         'city': 'Kyiv',
    #         'post_code': 55000,
    #     }
    #     self.shipping_method = 1
    #     self.payment_method = 1
    #     self.order_data_guest = {
    #         'email': self.email,
    #         'phone': self.phone,
    #         'shipping_address': self.address_dict,
    #         'shipping_method': self.shipping_method,
    #         'payment_method': self.payment_method,
    #     }
    #
    #     self.product_variation_1 = ProductVariation.objects \
    #         .select_related('product_item') \
    #         .prefetch_related('product_item__discount') \
    #         .first()
    #     self.product_variation_2 = ProductVariation.objects \
    #         .select_related('product_item') \
    #         .prefetch_related('product_item__discount') \
    #         .last()
    #
    #     discount_1 = self.create_discount(name='discount 1', discount_rate=10)
    #     discount_2 = self.create_discount(name='discount 2', discount_rate=20)
    #
    #     self.product_variation_1.product_item.discount.set([discount_1, discount_2])
    #     product_variation_1_discount_price = self.product_variation_1.product_item.get_discount_price()
    #
    #     self.product_data_1 = {
    #         'product_variation': self.product_variation_1.pk,
    #         'quantity': 3 if self.product_variation_1.qty_in_stock >= 3 else self.product_variation_1.qty_in_stock
    #     }
    #
    #     self.product_data_2 = {
    #         'product_variation': self.product_variation_2.pk,
    #         'quantity': 2 if self.product_variation_2.qty_in_stock >= 2 else self.product_variation_2.qty_in_stock
    #     }
    #
    #     product_variation_1_order_item_price = (
    #             product_variation_1_discount_price * self.product_data_1.get('quantity'))
    #     product_variation_2_order_item_price = (
    #             self.product_variation_2.product_item.get_discount_price() * self.product_data_2.get('quantity'))
    #     self.order_price = product_variation_1_order_item_price + product_variation_2_order_item_price
    #
    #     self.url_shopping_cart = 'shopping_cart_items-list'
    #     self.url_order_user = 'create_order_user'
    #     self.url_order_guest = 'create_order_guest'
    #     self.url_order_list = 'orders-list'
    #     self.url_order_detail = 'orders-detail'
    #     self.url_register_guest = 'register_guest'
    #     self.url_token = 'token_obtain_pair'
    #
    # def log_in_as_guest(self):
    #     response = self.client.post(reverse(self.url_register_guest), format='json')
    #     self.assertEqual(response.status_code, 201, 'Guest user must be register')
    #
    #     jwt = response.data['access']
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)
    #
    # def fill_in_shopping_cart(self):
    #     response = self.client.post(reverse(self.url_shopping_cart), self.product_data_1, format='json')
    #     response = self.client.post(reverse(self.url_shopping_cart), self.product_data_2, format='json')
    #     self.assertEqual(response.status_code, 201, 'Shopping cart items must be created successfully')
    #
    # def create_guest_order(self):
    #     self.log_in_as_guest()
    #     self.fill_in_shopping_cart()
    #
    #     response = self.client.post(reverse(self.url_order_guest), self.order_data_guest, format='json')
    #     return response

    def test_create_order(self):
        """

        """

        # Create order as a completely new guest user
        response = self.create_guest_order()
        self.assertEqual(response.status_code, 201, 'Order must be created successfully')
        self.assertEqual(response.data.get('order_price'), self.order_price,
                         f'Order price must be: {self.order_price}')

        # First order has been created by new guest user
        # Now he is registered and has an account in db
        #
        # Now try to create one more order as a guest using
        # credentials of registered user (same as first time)

        # Create order as a guest but with credentials of already registered user
        response = self.create_guest_order()
        self.assertEqual(response.status_code, 201, 'Order must be created successfully')
        self.assertEqual(response.data.get('order_price'), self.order_price,
                         f'Order price must be: {self.order_price}')

        # Now try to log in as user and check created orders. There have to be two orders for the user

        user = UserProfile.objects.get(email=self.email)
        password = '123456789'
        user.set_password(password)
        user.save()
        self.assertEqual(user.is_guest, False, 'user.is_guest must be False')

        data = {'email': self.email, 'password': password}

        response = self.client.post(reverse(self.url_token), data)
        self.assertEqual(response.status_code, 200, 'User must be able to log in')

        user_jwt = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_jwt)

        response = self.client.get(reverse(self.url_order_list), data)
        self.assertEqual(len(response.data), 2, 'User must have 2 orders')
        
        # Try to create third order as logged-in user 
        
        self.fill_in_shopping_cart()

        address = Address.objects \
                    .prefetch_related('address__user') \
                    .filter(address__user=user) \
                    .first()

        order_data_user = {
            'shipping_address': address.pk,
            'shipping_method': self.shipping_method,
            'payment_method': self.payment_method,
        }

        response = self.client.post(reverse(self.url_order_user), order_data_user, format='json')
        self.assertEqual(response.status_code, 201, 'Order must be created successfully')

        response = self.client.get(reverse(self.url_order_list), data)
        self.assertEqual(len(response.data), 3, 'User must have 3 orders')

    # def test_order_details_email(self):
    #
    #     def get_c():
    #         order_obj = 1
    #         order = {
    #             'id': 1,
    #             'date_created': 1,
    #             'price': 1,
    #         }
    #         shipping_address_obj = 1
    #         shipping_address = {
    #             'first_name': 1,
    #             'last_name': 1,
    #             'region': 1,
    #             'street': 1,
    #             'unit_number': 1,
    #             'city': 1,
    #             'country': 1,
    #         }
    #         order_items = [1, 1, 1]
    #         email = 'email@email.email'
    #
    #         context = dict(
    #             order=order,
    #             order_items=order_items,
    #             shipping_address=shipping_address,
    #             email=email,
    #         )
    #
    #         return context
    #
    #     email = 'email@email.email'
    #     phone = '+380985552288'
    #
    #     self.log_in_as_guest()
    #
    #     self.fill_in_shopping_cart()
    #
    #     order_data_guest = {
    #         'email': email,
    #         'phone': phone,
    #         'shipping_address': self.address_dict,
    #         'shipping_method': self.shipping_method,
    #         'payment_method': self.payment_method,
    #     }
    #
    #     response = self.client.post(reverse(self.url_order_guest), order_data_guest, format='json')
    #     context = get_c()
    #     send_order_email.apply(args=[email, context])
    #     sent_email = mail.outbox[0]
    #
    #     # Check that the email was sent
    #     self.assertEqual(len(mail.outbox), 1, 'email with must be sent')
    #
    #
    #     print(sent_email.alternatives[0][0])
    #     print(sent_email.alternatives[0][1])
