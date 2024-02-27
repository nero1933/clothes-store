from collections import OrderedDict

from django.core import mail
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ecommerce.models import Address, UserAddress
from ecommerce.tests import TestUser


class AddressTest:
    def init_address(self, user, is_default):
        data = {
            'first_name': 'Name',
            'last_name': 'Surname',
            'street': 'st',
            'unit_number': '1',
            'country': 'Ukraine',
            'region': 'K',
            'city': 'Kiev',
            'post_code': 55000,
        }

        address = Address.objects.create(**data)
        UserAddress.objects.create(address=address, user=user, is_default=is_default)

        return address

class AddressTestCase(APITestCase, TestUser, AddressTest):
    def setUp(self):
        self.user = self.init_user()
        self.jwt_access_token = self.login_user()
        self.address = self.init_address(self.user, is_default=False)

        self.data = {
            'address': {
                'first_name': 'John',
                'last_name': 'Doe',
                'street': 'CH',
                'unit_number': '123',
                'country': 'Ukraine',
                'region': 'KO',
                'city': 'Kiev',
                'post_code': 99123,
            }
        }

    def test_create_address(self):

        # Try to create users address
        response = self.client.post(
            reverse('addresses-list'),
            self.data,
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
        self.assertEqual(response_data, OrderedDict(self.data.get('address')), 'Users address data is not correct')

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
                'post_code': 54321,
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



