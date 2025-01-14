from rest_framework.reverse import reverse

from ecommerce.models import UserProfile, Address
from ecommerce.utils.tests.mixins import TestAPIOrder


class TestOrders(TestAPIOrder):

    def setUp(self):
        super().setUp()

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
