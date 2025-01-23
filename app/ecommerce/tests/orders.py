import uuid

from rest_framework.reverse import reverse

from ecommerce.models import UserProfile, Address, Order
from ecommerce.utils.tests.mixins import TestAPIOrder


class TestOrders(TestAPIOrder):

    def setUp(self):
        super().setUp()

    def test_create_order(self):
        """

        """

        def check_order_access(order_pk: Order.pk):
            # log out
            self.client.credentials()

            # Create new user
            test_email = uuid.uuid4().hex + '@domain.com'
            test_password = '123456789'
            test_user = UserProfile.objects.create_user(test_email, 'John', 'Doe', test_password)
            test_user.is_active = True
            test_user.save()
            self.assertEqual(test_user.is_guest, False, 'user.is_guest must be False')

            test_data = {'email': test_email, 'password': test_password}

            r = self.client.post(reverse(self.url_token), test_data)
            self.assertEqual(r.status_code, 200, 'User must be able to log in')

            test_user_jwt = r.data.get('access')
            auth = {'HTTP_AUTHORIZATION': 'Bearer ' + test_user_jwt}

            # User can't have access to order which he didn't create
            r = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_pk}), format='json', **auth)
            self.assertEqual(r.status_code, 404,
                             "User can't have access to order which he didn't create")

            # Guest can't have access to order which he didn't create
            r = self.client.post(reverse(self.url_register_guest), format='json')
            test_guest_jwt = r.data['access']
            auth = {'HTTP_AUTHORIZATION': 'Bearer ' + test_guest_jwt}

            r = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_pk}), format='json', **auth)
            self.assertEqual(r.status_code, 404,
                             "Guest can't have access to order which he didn't create")

            return None

        # Create order as a completely new guest user
        response = self.create_guest_order()
        self.assertEqual(response.status_code, 201, 'Order must be created successfully')
        self.assertEqual(response.data.get('order_price'), self.order_price,
                         f'Order price must be: {self.order_price}')

        order_id = response.data.get('id')

        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}), format='json')
        self.assertEqual(response.status_code, 200,
                         'Order details must be displayed to account which'
                         ' became user after creating order account successfully')

        # Check that user and guest (which didn't create order) have no access to order
        check_order_access(order_id)

        # First order has been created by new guest user
        # Now he is registered and has an account in db
        #
        # Now try to create one more order as a guest using
        # credentials of registered user (same as first time)

        # Create order as a guest but with credentials of already registered user
        response = self.create_guest_order()
        order_id = response.data.get('id')
        self.assertEqual(response.status_code, 201, 'Order must be created successfully')
        self.assertEqual(response.data.get('order_price'), self.order_price,
                         f'Order price must be: {self.order_price}')

        # Guest (which is user, but creates order while not logged in) must view his order details
        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}), format='json')
        self.assertEqual(response.status_code, 200,
                         'Order details must be displayed to guest account (of existing user) successfully')

        # Check that user and guest (which didn't create order) have no access to order
        check_order_access(order_id)

        # Now try to log in as user and check created orders. There have to be two orders for the user

        user = UserProfile.objects.get(email=self.email)
        password = '123456789'
        user.set_password(password)
        user.save()
        self.assertEqual(user.is_guest, False, 'user.is_guest must be False')

        self.login_as_user()

        response = self.client.get(reverse(self.url_order_list))
        self.assertEqual(len(response.data), 2, 'User must have 2 orders')

        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}), format='json')
        self.assertEqual(response.status_code, 200,
                         'Order details (of order made by user when he was logged in '
                         'as guest) must be displayed to user account successfully')

        # Check that user and guest (which didn't create order) have no access to order
        check_order_access(order_id)
        
        # Try to create third order as logged-in user
        self.login_as_user()
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
        order_id = response.data.get('id')
        self.assertEqual(response.status_code, 201, 'Order must be created successfully')

        response = self.client.get(reverse(self.url_order_list))
        self.assertEqual(len(response.data), 3, 'User must have 3 orders')

        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}), format='json')
        self.assertEqual(response.status_code, 200,
                         'Order details must be displayed to user account successfully')

        order_item = response.data.get('order_item')
        res = ['id', 'product_variation', 'product_name', 'product_code', 'product_gender', 'product_size',
               'product_price', 'quantity', 'price', 'review_id', 'review_url', 'product_url', 'main_image']

        self.assertEqual(list(order_item[0].keys()), res,
                         f'Order item must contain every key from this list {res}')

    def test_main_image(self):
        response = self.create_guest_order()
        self.assertEqual(response.status_code, 201, 'Order must be created successfully')

        order_id = response.data.get('id')

        response = self.client.get(reverse(self.url_order_detail, kwargs={'pk': order_id}), format='json')
        self.assertEqual(response.status_code, 200,
                         'Order details must be displayed to guest account successfully')

        order_items = response.data.get('order_item')

        img_1 = order_items[0].get('main_image', None)
        img_2 = order_items[1].get('main_image', None)

        self.assertTrue(self.is_valid_url(img_1.get('url', '')),
                        'First order image must be displayed to guest account successfully')
        self.assertTrue(img_2 is None,
                         'Second order image must be None')

    def test_order_access(self):
        pass
