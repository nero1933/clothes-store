from datetime import timedelta

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.db import IntegrityError
from django.http import Http404
from django.utils import timezone

from rest_framework import status, mixins
from rest_framework.decorators import api_view, action
from rest_framework.generics import CreateAPIView, get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from app import settings
from ecommerce.models import UserProfile, UserProfileManager
from ecommerce.serializers import RegisterUserSerializer, PasswordResetSerializer, PasswordSerializer, \
    UserProfileSerializer, RegisterGuestSerializer
from ecommerce.utils.email.senders import RegistrationEmail, PasswordResetEmail
from ecommerce.utils.keys_managers.keys_encoders import KeyEncoder


class LoginView(APIView):
    """
    User authentication.

    Generation of JWT token and setting refresh token into HttpOnly cookie.
    """

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        # access_token['is_guest'] = user.is_guest

        response = Response(
            {
                'access_token': str(access_token),
                'id': user.id,
                'name': user.first_name,
                'is_guest': user.is_guest,
            },
            status=status.HTTP_200_OK,
        )

        expires = timezone.now() + timedelta(days=7)

        response.set_cookie(
            'refresh_token', str(refresh),
            httponly=True,
            # secure=settings.SECURE_SSL_REDIRECT, # use in production
            expires=expires,
            samesite='Strict',
        )

        return response


class LogoutView(APIView):
    """
    Logout user.

    Delete refresh token from HttpOnly cookie.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        response = Response(
            {'detail': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('refresh_token')
        return response


class TokenRefreshView(APIView):
    """
    Update access token.

    Use refresh token from HttpOnly cookie to generate new access token.
    """

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'detail': 'Refresh token not found in cookies'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response(
                {'access_token': access_token},
                status=status.HTTP_204_NO_CONTENT
            )
        except TokenError:
            return Response(
                {'detail': 'Invalid refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['PATCH'])
def register_user_confirmation(request, *args, **kwargs):
    """
    Confirm registration of a user with a confirmation email.
    """
    confirmation_key = settings.USER_CONFIRMATION_KEY.format(token=kwargs['token'])
    user = cache.get(confirmation_key) or {}

    if user_id := user.get('user_id'):
        user = get_object_or_404(UserProfile, pk=user_id)
        user.is_active = True
        user.save(update_fields=['is_active'])
        cache.delete(confirmation_key)
        return Response(
            {'message': 'User is registered successfully!'},
            status=status.HTTP_204_NO_CONTENT
        )
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterUserAPIView(CreateAPIView,
                          RegistrationEmail,
                          KeyEncoder):
    """
    View for user registration.
    """
    serializer_class = RegisterUserSerializer

    confirmation_key = settings.USER_CONFIRMATION_KEY
    timeout = settings.USER_CONFIRMATION_TIMEOUT

    def post(self, request, *args, **kwargs):
        try:
            response = self.create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                'Email already exists.',
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        user_id = response.data.get('id', None)
        user_email = response.data.get('email', None)

        confirmation_key, token = self.create_confirmation_key_and_token() # method from KeyEncoder
        cache.set(confirmation_key, {'user_id': user_id}, timeout=self.timeout) # set key to cache
        self.send_registration_link(request, user_email, token) # method from RegistrationEmail

        return response


class RegisterGuestAPIView(CreateAPIView):
    """
    View for guest registration.
    """
    serializer_class = RegisterGuestSerializer

    def post(self, request, *args, **kwargs):
        user_profile_manager = UserProfileManager()
        user = user_profile_manager.create_guest()

        if not user:
            return Response(
                {'detail': 'Could not create guest user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response(
            {
                'access_token': access_token,
                'email': user.email,
            },
            status=status.HTTP_201_CREATED
        )

        expires = timezone.now() + timedelta(days=7)

        response.set_cookie(
            'refresh_token', str(refresh),
            httponly=True,
            # secure=settings.SECURE_SSL_REDIRECT, # use in production
            expires=expires,
            samesite='Strict',
        )

        return response


class PasswordResetAPIView(APIView,
                           PasswordResetEmail,
                           KeyEncoder):
    """
    View for password reset.

    Takes 'email' from serializer and sends an email with a link to proceed password reset.
    """
    confirmation_key = settings.PASSWORD_RESET_KEY # const from KeyEncoder
    timeout = settings.PASSWORD_RESET_TIMEOUT # const from KeyEncoder

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data['email']
        user_id = get_object_or_404(UserProfile, email=user_email).pk

        confirmation_key, token = self.create_confirmation_key_and_token() # method from KeyEncoder
        cache.set(confirmation_key, {'user_id': user_id}, timeout=self.timeout) # set key to cache
        self.send_password_reset_link(request, user_email, token) # method from RegistrationEmail

        return Response(
            {'message': 'Email sent. Check your mailbox!'},
            status=status.HTTP_204_NO_CONTENT
        )


class PasswordResetNewPasswordAPIView(mixins.UpdateModelMixin,
                                      GenericAPIView):
    """
    View for password reset.
    """
    serializer_class = PasswordSerializer

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
                'Link is expired.',
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    """
    ViewSet for user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'options']
    lookup_field = 'pk'

    def get_object(self):
        user = self.request.user
        if user.pk != int(self.kwargs['pk']):
            raise Http404

        return user

    @action(detail=True, methods=['patch'], url_path='set-password')
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
