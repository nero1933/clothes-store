import re

from django.core import mail
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ecommerce.models import UserProfile


def get_link_from_message(message):
    regex = r"(?P<url>https?://[^\s]+)"
    match = re.search(regex, message)
    link = match.group("url")
    return link


class TestUser:
    email = 'test@test.com'
    password = '12345678'
    user = None
    jwt_access_token = None

    def init_user(self):
        user = UserProfile.objects.create_user(
            email=self.email,
            first_name='test',
            last_name='test',
            phone='+380951112233',
            password=self.password
        )

        user.is_active = True
        user.save()

        return user

    def login_user(self):
        data = {'email': self.email, 'password': self.password}

        response = self.client.post(reverse('token_obtain_pair'), data)
        return response.data.get('access')


class UserTestCase(APITestCase, TestUser):

    def setUp(self):
        self.user = self.init_user()
        self.jwt_access_token = self.login_user()

    def test_register_user(self):
        """
        Try to register user and follow the confirmation link.
        """

        data = {
            "email": "tests@tests.com",
            "first_name": "tests",
            "last_name": "tests",
            "phone": '+380956665544',
            "password": '12345678',
            "password_confirmation": '12345678',
        }

        # Try to register
        response = self.client.post(reverse('register_user'), data, format='json')
        user_id = response.data.get('id')
        user = get_object_or_404(UserProfile, pk=user_id)

        # Check that the email was sent
        self.assertEqual(len(mail.outbox), 1, 'email with a verification link must be sent')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Code must be 201')

        # Check 'is_active' status of created user before opening link from email
        self.assertEqual(user.is_active, False,
                         'Before opening link from email "is_active" status of the user must be True')

        # Get confirmation link from message
        message = mail.outbox[0].body
        link = get_link_from_message(message)

        # Follow the confirmation link
        response = self.client.patch(link, format='json')
        user = get_object_or_404(UserProfile, pk=user_id)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Code must be 204')

        # Check 'is_active' status of created user after opening link from email
        self.assertEqual(user.is_active, True, 'After opening link from email "is_active" status of the user must be True')


    def test_password_reset(self):
        """
        Try to reset password, follow the confirmation link and enter nwe password.
        """

        data = {'email': 'test@test.com', 'password': '12345678'}

        # Try to log in
        response = self.client.post(reverse('token_obtain_pair'), data)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Try to reset password
        response = self.client.post(reverse('password_reset'), data, format='json')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Code must be 204')

        # Get confirmation link from message
        message = mail.outbox[0].body
        link = get_link_from_message(message)

        data = {'password': '87654321', 'password_confirmation': '87654321'}

        # Follow the confirmation link
        response = self.client.patch(link, data, format='json')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Code must be 204')

        data = {'email': 'test@test.com', 'password': '87654321'}

        # Try to log in with new credentials
        response = self.client.post(reverse('token_obtain_pair'), data)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')


    def test_user_view_set(self):

        data = {'id': 4, 'email': 'test@test.com', 'first_name': 'test', 'last_name': 'test', 'phone': '+380951112233'}
        kwargs = {'pk': self.user.pk}

        response = self.client.get(
            reverse('users-detail', kwargs=kwargs),
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Check that the response has right data
        self.assertEqual(response.data, data, f'data must be {data}')

        new_particular_data = {'first_name': 'John', 'last_name': 'Doe'}
        new_data = {'id': 4, 'email': 'test@test.com', 'first_name': 'John', 'last_name': 'Doe', 'phone': '+380951112233'}

        response = self.client.patch(
            reverse('users-detail', kwargs=kwargs),
            new_particular_data,
            HTTP_AUTHORIZATION=f'Bearer {self.jwt_access_token}',
            format='json'
        )

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        # Check that the response has right data
        self.assertEqual(response.data, new_data, f'data must be {new_data}')