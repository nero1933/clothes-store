import re
from time import sleep

from django.core import mail
from django.core.cache import cache
from django.test import override_settings

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse

from ecommerce.models import UserProfile
from ecommerce.utils.tests.mixins import TestAPIEcommerce


def get_link_from_message(message) -> str:
    regex = r"(?P<url>https?://[^\s]+)"
    match = re.search(regex, message)
    link = match.group("url")
    return link


def extract_token_form_url(url) -> str:
    regex = r'/(activate|reset-password)/([\w\d]+)/'
    match = re.search(regex, url)
    token = match.group(2)
    return token


class UserTestCase(TestAPIEcommerce):

    def setUp(self):
        self.user = self.create_user()
        self.jwt_access_token = self.get_jwt_access_token()


    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_register_user(self):
        """
        Try to register user and follow the confirmation link.
        """
        cache.clear()

        data = {
            "email": "new-test@test.test",
            "first_name": "tests",
            "last_name": "tests",
            "password": '12345678',
            "password_confirmation": '12345678',
        }

        # Try to register
        response = self.client.post(reverse('register_user'), data, format='json')
        user_id = response.data.get('id')
        user = get_object_or_404(UserProfile, pk=user_id)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Code must be 201')

        # Check 'is_active' status of created user before opening link from email
        self.assertEqual(user.is_active, False,
                         'Before opening link from email "is_active" status of the user must be True')

        # Check that the email was sent
        self.assertEqual(len(mail.outbox), 1, 'Email must be sent')

        # Get confirmation link from message
        message = mail.outbox[0].body
        link = get_link_from_message(message)

        # Extract token
        conf_token = extract_token_form_url(link)

        # Create link to API endpoint with token
        link = reverse('activate_user', kwargs={'conf_token': conf_token})

        # Follow the link to API
        response = self.client.post(link, format='json')
        user = get_object_or_404(UserProfile, pk=user_id)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Code must be 204')

        # Check 'is_active' status of created user after opening link from email
        self.assertEqual(user.is_active, True, 'After opening link from email "is_active" status of the user must be True')


    def test_password_reset(self):
        """
        Try to reset password, follow the confirmation link and enter new password.
        """

        data = {'email': 'test@test.com', 'password': '12345678'}

        # Try to log in
        response = self.client.post(reverse('token_obtain_pair'), data)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Try to reset password
        data = {'email': 'test@test.com'}
        response = self.client.post(reverse('forgot_password'), data, format='json')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Code must be 204')

        # Check that email was sent
        self.assertEqual(len(mail.outbox), 1, 'Email must be sent')

        # Get confirmation link from message
        message = mail.outbox[0].body
        link = get_link_from_message(message)

        # Extract token
        conf_token = extract_token_form_url(link)

        # Create link to API endpoint with token
        link = reverse('reset_password', kwargs={'conf_token': conf_token})

        data = {'password': '87654321', 'password_confirmation': '87654321'}

        # Follow the link to API
        response = self.client.patch(link, data, format='json')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Code must be 204')

        data = {'email': 'test@test.com', 'password': '87654321'}

        # Try to log in with new credentials
        response = self.client.post(reverse('token_obtain_pair'), data)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')
    #
    #
    # def test_user_view_set(self):
    #
    #     data = {'email': 'test@test.com', 'first_name': 'test', 'last_name': 'test'}
    #     kwargs = {'pk': self.user.pk}
    #
    #     response = self.client.get(
    #         reverse('users-detail', kwargs=kwargs),
    #         data,
    #         HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
    #         format='json'
    #     )
    #
    #     response.data.pop('id')
    #
    #     # Check that the response has a success status code
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')
    #
    #     # Check that the response has right data
    #     self.assertEqual(response.data, data, f'data must be {data}')
    #
    #     new_particular_data = {'first_name': 'John', 'last_name': 'Doe'}
    #     new_data = {'email': 'test@test.com', 'first_name': 'John', 'last_name': 'Doe'}
    #
    #     response = self.client.patch(
    #         reverse('users-detail', kwargs=kwargs),
    #         new_particular_data,
    #         HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
    #         format='json'
    #     )
    #
    #     response.data.pop('id')
    #
    #     # Check that the response has a success status code
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')
    #
    #     # Check that the response has right data
    #     self.assertEqual(response.data, new_data, f'data must be {new_data}')
