from django.core.cache import cache
from django.db import IntegrityError

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response

from app import settings
from ecommerce.models import UserProfile
from ecommerce.serializers import RegisterUserSerializer
from ecommerce.utils.email.senders import SendRegistrationEmail


class RegisterUserAPIView(CreateAPIView, SendRegistrationEmail):
    """
    View for registration.
    """
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = self.create(request, *args, **kwargs)
        except IntegrityError:
            return Response("Email already exists.",
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        user_id = response.data.get('id', None)
        user_email = response.data.get('user_email', None)
        self.send_registration_link(request, user_id, user_email)
        return response


@api_view(['PATCH'])
def confirm_register_user(request, token):
    confirmation_key = settings.USER_CONFIRMATION_KEY.format(token=token)
    user = cache.get(confirmation_key) or {}

    if user_id := user.get('user_id'):
        user = get_object_or_404(UserProfile, pk=user_id)
        user.is_active = True
        user.save(update_fields=['is_active'])
        cache.delete(confirmation_key)
        return Response({'message': 'Successfully registered', "data": request.data}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

