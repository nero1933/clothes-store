import re

from django.core import mail
from django.core.cache import cache
from django.test import override_settings

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse

from app import settings
from ecommerce.models import UserProfile
from ecommerce.utils.tests.mixins import TestAPIEcommerce


def extract_token_form_url(url) -> str:
    regex = r'/(activate|reset-password)/([\w\d]+)/'
    match = re.search(regex, url)
    token = match.group(2)
    return token


def get_count_and_conf_token(count: int):
    # Get confirmation link from message
    message = mail.outbox[count].body

    # Extract token
    conf_token = extract_token_form_url(message)

    # Increase count by one (one mail was send)
    count += 1

    return count, conf_token


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

        # Extract token
        conf_token = extract_token_form_url(message)

        # Create link to API endpoint with token
        link = reverse('activate_user', kwargs={'conf_token': conf_token})

        # Follow the link to API
        response = self.client.post(link, format='json')
        user = get_object_or_404(UserProfile, pk=user_id)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Check 'is_active' status of created user after opening link from email
        self.assertEqual(user.is_active, True, 'After opening link from email "is_active" status of the user must be True')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_activate_user(self):
        cache.clear()
        max_attempts = settings.USER_CONFIRMATION_MAX_ATTEMPTS
        count = 0

        data = {
            "email": "new-test@test.test",
            "first_name": "tests",
            "last_name": "tests",
            "password": '12345678',
            "password_confirmation": '12345678',
        }

        # Try to register user
        response = self.client.post(reverse('register_user'), data, format='json')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Code must be 201')

        count, conf_token = get_count_and_conf_token(count)

        # Create dictionary to store all activation attempts with conf_token
        count_dict: dict[str: str] = {str(count): conf_token}

        data = {
            "email": "new-test@test.test",
            "password": "12345678",
        }
        while count < max_attempts:
            response = self.client.post(reverse('login'), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                             'Code must be 403')

            count, conf_token = get_count_and_conf_token(count)

            # Add count with conf_token
            count_dict.setdefault(str(count), conf_token)

        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS,
                         'Code must be 429')

        for k, v in count_dict.items():
            response = self.client.post(reverse('activate_user',
                                                kwargs={'conf_token': v}),
                                        format='json')
            if int(k) != max_attempts:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                                 'If link is old, and a newer link was send, code must be 400')
            else:
                self.assertEqual(response.status_code, status.HTTP_200_OK,
                                 'If link is active, last sent and token in correct, code must be 200')

        # Try to log in
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Code must be 200')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_reset_password(self):
        """
        Try to reset password, follow the confirmation link and enter new password.
        """

        data = {'email': 'test@test.com', 'password': '12345678'}

        # Try to log in
        response = self.client.post(reverse('login'), data)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Try to reset password
        data = {'email': 'test@test.com'}
        response = self.client.post(reverse('forgot_password'), data, format='json')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Check that email was sent
        self.assertEqual(len(mail.outbox), 1, 'Email must be sent')

        # Get confirmation link from message
        message = mail.outbox[0].body

        # Extract token
        conf_token = extract_token_form_url(message)

        # Create link to API endpoint with token
        link = reverse('reset_password', kwargs={'conf_token': conf_token})

        data = {'password': '87654321', 'password_confirmation': '87654321'}

        # Follow the link to API
        response = self.client.patch(link, data, format='json')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        data = {'email': 'test@test.com', 'password': '87654321'}

        # Try to log in with new credentials
        response = self.client.post(reverse('login'), data)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_reset_password_max_attempts(self):
        cache.clear()
        max_attempts = settings.RESET_PASSWORD_MAX_ATTEMPTS
        count = 0
        count_dict: dict[str: str] = {}
        data = {'email': 'test@test.com'}
        reset_password_data = {'password': '87654321', 'password_confirmation': '87654321'}


        while count < max_attempts:
            # Try to get email
            response = self.client.post(reverse('forgot_password'),
                                        data,
                                        format='json')

            count, conf_token = get_count_and_conf_token(count)

            # Set count and token to dict
            count_dict.setdefault(str(count), conf_token)

        response = self.client.post(reverse('forgot_password'),
                                    data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS,
                         'Code must be 429')


        for k, v in count_dict.items():
            # Try to reset password
            response = self.client.patch(reverse('reset_password',
                                                kwargs={'conf_token': v}),
                                        reset_password_data,
                                        format='json')

            if int(k) != max_attempts:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                                 f'If link is old, and a newer link was send, code must be 400')
            else:
                self.assertEqual(response.status_code, status.HTTP_200_OK,
                                 'If link is active, last sent and token in correct, code must be 200')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_user_activation_while_reset_password(self):
        cache.clear()

        data = {
            "email": "new-test@test.test",
            "first_name": "tests",
            "last_name": "tests",
            "password": '12345678',
            "password_confirmation": '12345678',
        }

        forgot_password_data = {"email": "new-test@test.test"}

        reset_password_data = {
            'password': '87654321',
            'password_confirmation': '87654321'
        }

        # Try to register
        response = self.client.post(reverse('register_user'), data, format='json')
        user_id = response.data.get('id')
        user = get_object_or_404(UserProfile, pk=user_id)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         'Code must be 201')

        # Check 'is_active' status of created user before opening link from email
        self.assertEqual(user.is_active, False,
                         'Before opening link from email "is_active" status of the user must be True')

        response = self.client.post(reverse('forgot_password'),
                                    forgot_password_data,
                                    format='json')

        message = mail.outbox[1].body # One means second mail, first was sent while registration
        conf_token = extract_token_form_url(message)

        response = self.client.patch(reverse('reset_password',
                                            kwargs={'conf_token': conf_token}),
                                    reset_password_data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Code must be 200')

        user = get_object_or_404(UserProfile, pk=user_id)

        self.assertEqual(user.is_active, True, 'User must be active')


    def test_user_view_set(self):

        data = {'email': 'test@test.com', 'first_name': 'test', 'last_name': 'test'}
        kwargs = {'pk': self.user.pk}

        response = self.client.get(
            reverse('users-detail', kwargs=kwargs),
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        response.data.pop('id')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Check that the response has right data
        self.assertEqual(response.data, data, f'data must be {data}')

        new_particular_data = {'first_name': 'John', 'last_name': 'Doe'}
        new_data = {'email': 'test@test.com', 'first_name': 'John', 'last_name': 'Doe'}

        response = self.client.patch(
            reverse('users-detail', kwargs=kwargs),
            new_particular_data,
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        response.data.pop('id')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Check that the response has right data
        self.assertEqual(response.data, new_data, f'data must be {new_data}')
