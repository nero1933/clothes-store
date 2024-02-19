from django.core.cache import cache
from django.db import IntegrityError

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, get_object_or_404, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app import settings
from ecommerce.models import UserProfile
from ecommerce.serializers import RegisterUserSerializer, PasswordResetSerializer, PasswordResetNewPasswordSerializer
from ecommerce.utils.email.senders import RegistrationEmail, PasswordResetEmail
from ecommerce.utils.keys_managers.keys_encoders import KeyEncoder


@api_view(['PATCH'])
def register_user_confirmation(request, *args, **kwargs):
    """
    test.
    """
    confirmation_key = settings.USER_CONFIRMATION_KEY.format(token=kwargs['token'])
    user = cache.get(confirmation_key) or {}

    if user_id := user.get('user_id'):
        user = get_object_or_404(UserProfile, pk=user_id)
        user.is_active = True
        user.save(update_fields=['is_active'])
        cache.delete(confirmation_key)
        return Response({'message': 'User is registered successfully!', "data": request.data}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterUserAPIView(CreateAPIView, RegistrationEmail, KeyEncoder):
    """
    View for registration.
    """
    serializer_class = RegisterUserSerializer

    confirmation_key = settings.USER_CONFIRMATION_KEY
    timeout = settings.USER_CONFIRMATION_TIMEOUT

    def post(self, request, *args, **kwargs):
        try:
            response = self.create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                "Email already exists.",
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        user_id = response.data.get('id', None)
        user_email = response.data.get('user_email', None)

        confirmation_key, token = self.create_confirmation_key_and_token() # method from PasswordResetKeyEncoder
        cache.set(confirmation_key, {'user_id': user_id}, timeout=self.timeout) # set key to cache
        self.send_registration_link(request, user_id, user_email, token) # method from RegistrationEmail

        return response


class PasswordResetAPIView(APIView, PasswordResetEmail, KeyEncoder):
    """
    View for password reset.

    Takes 'email' from serializer and sends to it a mail with a link to proceed password reset.
    """
    confirmation_key = settings.PASSWORD_RESET_KEY
    timeout = settings.PASSWORD_RESET_TIMEOUT

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data['email']
        user_id = get_object_or_404(UserProfile, email=user_email).pk

        confirmation_key, token = self.create_confirmation_key_and_token() # method from PasswordResetKeyEncoder
        cache.set(confirmation_key, {'user_id': user_id}, timeout=self.timeout) # set key to cache
        self.send_password_reset_link(request, user_id, user_email, token) # method from RegistrationEmail

        return Response({'message': 'Email send. Check your mailbox!'}, status=status.HTTP_204_NO_CONTENT)


class PasswordResetNewPasswordAPIView(UpdateAPIView):
    serializer_class = PasswordResetNewPasswordSerializer

    def get_object(self):
        confirmation_key = settings.PASSWORD_RESET_KEY.format(token=self.kwargs['token'])
        data = cache.get(confirmation_key) or {}

        if user_id := data.get('user_id'):
            user = get_object_or_404(UserProfile, pk=user_id)
            cache.delete(confirmation_key)
            return user

    def patch(self, request, *args, **kwargs):
        try:
            self.partial_update(request, *args, **kwargs)
            return Response(
                {'message': 'Password was changed successfully!'},
                status=status.HTTP_204_NO_CONTENT
            )
        except TimeoutError:
            return Response(
                "Link has been expired.",
                status=status.HTTP_400_BAD_REQUEST
            )
