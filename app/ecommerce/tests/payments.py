import uuid
from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.reverse import reverse

from ecommerce.models import UserProfile, ProductItem, Payment
from ecommerce.utils.tests.mixins import TestAPIOrder
from ecommerce.views.payments import CreateCheckoutSessionAPIView


class TestPayments(TestAPIOrder):

    def setUp(self):
        super().setUp()

        self.url_payment_checkout = 'payment_checkout'

        product_item_1 = ProductItem.objects.get(product_variation=self.product_variation_1)
        product_item_1.stripe_price_id = 'price_1H2gJvFxrQk8dXzA1p'
        product_item_2 = ProductItem.objects.get(product_variation=self.product_variation_2)
        product_item_2.stripe_price_id = 'price_1H2gJvFxrQk8dXzA1f'

        product_item_1.save()
        product_item_2.save()

    @patch('stripe.checkout.Session.create')  # Mocking the Stripe API
    def test_create_checkout_session_success(self, mock_stripe_session_create):

        # Arrange: Create a mock session object
        mock_session = MagicMock()
        mock_session.id = 'cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u'
        mock_session.url = 'https://checkout.stripe.com/pay/cs_test_12345'

        # Set the mock to return the session object
        mock_stripe_session_create.return_value = mock_session

        # Create a test order and payment
        response = self.create_guest_order()
        order_id = response.data.get('id', None)

        # Ensure that order_id is valid
        self.assertIsNotNone(order_id)

        response = self.client.post(reverse(self.url_payment_checkout, args=[order_id]))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['checkout_session_id'], 'cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u')
        self.assertEqual(response.data['checkout_session_url'], 'https://checkout.stripe.com/pay/cs_test_12345')

    def test_get_line_items(self):
        """ Test for get_line_items method in CreateCheckoutSessionAPIView """

        # Create an instance of the view
        view = CreateCheckoutSessionAPIView()

        # Manually attach a request with the user to the view instance
        self.client.force_authenticate(user=self.user)
        request = self.client.request().wsgi_request
        request.user = self.user
        view.request = request

        response = self.create_guest_order()
        order_id = response.data.get('id', None)

        # Call the get_line_items method
        line_items = view.get_line_items(order_id=order_id)

        self.assertEqual(
            line_items,
            [{'price': 'price_1H2gJvFxrQk8dXzA1p', 'quantity': 3},
            {'price': 'price_1H2gJvFxrQk8dXzA1f', 'quantity': 2}],
            'Line items must display price & quantity'
        )

    # def test_payment(self):
    #     response = self.create_guest_order()
    #     order_id = response.data.get('id', None)
    #     response = self.client.post(reverse(self.url_payment_checkout, args=[order_id]), {})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    #     # checkout_session_id = response.data.get('checkout_session_id', None)
    #     # checkout_session_url = response.data.get('checkout_session_url', None)
    #     # print(checkout_session_id, checkout_session_url)
    #     self.assertEqual(response.data['checkout_session_id'], 'cs_test_12345')
    #     self.assertEqual(response.data['checkout_session_url'], 'https://checkout.stripe.com/pay/cs_test_12345')

