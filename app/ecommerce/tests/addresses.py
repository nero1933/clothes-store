from collections import OrderedDict

from rest_framework import status
from rest_framework.reverse import reverse

from ecommerce.utils.tests.mixins import TestAPIEcommerce


class AddressTestCase(TestAPIEcommerce):
    def setUp(self):
        self.user = self.create_user()
        self.jwt_access_token = self.get_jwt_access_token()
        self.address = self.create_address(self.user, is_default=False)

    def test_create_address(self):
        data = {
            'address': {
                'first_name': 'John',
                'last_name': 'Doe',
                'street': 'CH',
                'unit_number': '123',
                'country': 'Ukraine',
                'region': 'KO',
                'city': 'Kiev',
                'post_code': '99123',
                'phone_number': '+380993332211'
            }
        }

        # Try to create users address
        response = self.client.post(
            reverse('addresses-list'),
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Code must be 201')

        # Try to get created users address
        response = self.client.get(
            reverse('addresses-list'),
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Get 'address' dict
        response_data = response.data[1].get('address')
        response_data.pop('id')

        # Check that the 'address' dict from response is equal to address from self.data
        self.assertEqual(response_data, OrderedDict(data.get('address')), 'Users address data is not correct')

    def test_update_address(self):
        data = {
            'address': {
                'first_name': '1',
                'last_name': '2',
                'street': '3',
                'unit_number': '4',
                'country': 'France',
                'region': '5',
                'city': '6',
                'post_code': '54321',
                'phone_number': '+380993332210'
            },
        }

        # Get all user addresses
        response = self.client.get(
            reverse('addresses-list'),
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        address_id = response.data[0].get('address').get('id')

        response = self.client.patch(
            reverse('addresses-detail', kwargs={'pk': address_id}),
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Check that address id is the same
        self.assertEqual(response.data.get('address').get('id'), address_id, 'Address id must be the same')

        response_data = response.data.get('address')
        response_data.pop('id')

    def test_delete_address(self):

        # Get all user addresses
        response = self.client.get(
            reverse('addresses-list'),
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        address_id = response.data[0].get('address').get('id')

        # Delete user address
        response = self.client.delete(
            reverse('addresses-detail', kwargs={'pk': address_id}),
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Code must be 200')

        # Get all user addresses
        response = self.client.get(
            reverse('addresses-list'),
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        # Check that user don't have any addresses
        self.assertEqual(len(response.data), 0, 'Address id must be the same')



