from datetime import timedelta

from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.http import Http404
from django.utils import timezone

from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from app import settings
from ecommerce.models import UserProfile, UserProfileManager
from ecommerce.serializers import RegisterUserSerializer, \
    UserProfileSerializer, RegisterGuestSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from ecommerce.utils.email.send_email import ActivationEmail
from ecommerce.utils.email.senders import RegistrationEmail, PasswordResetEmail
from ecommerce.utils.confirmation_managers.confirmation_managers import ConfirmationManager, ConfirmationCacheManager


class LoginView(APIView, RegistrationEmail):
    """
    User authentication.

    Generation of JWT token and setting refresh token into HttpOnly cookie.
    """

    def handle_inactive_user(self, user):
        confirmation_flag_template = settings.USER_CONFIRMATION_FLAG_TEMPLATE
        confirmation_flag_template.format(user_id=user.id)
        confirmation_flag = cache.get(confirmation_flag_template)

        error = ''
        if confirmation_flag:
            error = 'Activate your account by opening link from email!'
        else:
            error = 'Activate your account, new email was send!'
            self.send_registration_link()

        return Response(
            {'error': error},
            status=status.HTTP_403_FORBIDDEN
        )

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = UserProfile.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            inactive_user_response = self.handle_inactive_user(user)
            return inactive_user_response
            # return Response(
            #     {'error': 'Your account is not activated. Please check your email.'},
            #     status=status.HTTP_403_FORBIDDEN
            # )

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

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

    Deletes refresh token from HttpOnly cookie.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        response = Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('refresh_token')
        return response


class TokenRefreshView(APIView):
    """
    Update access token.

    Uses refresh token from HttpOnly cookie to generate new access token.
    """

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'error': 'Refresh token not found in cookies'},
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
                {'error': 'Invalid refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
def activate_user(request, *args, **kwargs):
    """
    Confirm registration of a user with a confirmation email.
    """
    confirmation_key = settings.USER_CONFIRMATION_KEY_TEMPLATE.format(
        conf_token=kwargs['conf_token']
    )
    user = cache.get(confirmation_key, {})

    if user_id := user.get('user_id'):
        user = get_object_or_404(UserProfile, pk=user_id)
        user.activate()
        cache.delete(confirmation_key)
        return Response(
            {'message': 'User is registered successfully!'},
            status=status.HTTP_204_NO_CONTENT
        )
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterUserAPIView(CreateAPIView,
                          ActivationEmail):
    """
    View for user registration.
    """
    serializer_class = RegisterUserSerializer

    # confirmation_key_template = settings.USER_CONFIRMATION_KEY_TEMPLATE
    # confirmation_flag_template = settings.USER_CONFIRMATION_FLAG_TEMPLATE
    # timeout = settings.USER_CONFIRMATION_TIMEOUT

    def __init__(self, *args, **kwargs):
        # Initialize parent classes explicitly
        super().__init__(*args, **kwargs)
        ConfirmationManager.__init__(self)

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                response = self.create(request, *args, **kwargs)

                user_id = response.data.get('id', None)
                user_email = response.data.get('email', None)

                self.prepare_and_send_confirmation_email(user_email, user_id)

                return response

        except IntegrityError:
            return Response(
                {'error', 'Email already exists.'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        except Exception as e:
            return Response(
                {'error': f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
                {'error': 'Could not create guest user'},
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


class ForgotPasswordAPIView(APIView,
                           PasswordResetEmail,
                           ConfirmationManager):
    """
    View for password reset.

    Takes 'email' from serializer and sends an email with a link to proceed password reset.
    """
    confirmation_key_template = settings.PASSWORD_RESET_KEY # const from KeyEncoder
    timeout = settings.PASSWORD_RESET_TIMEOUT # const from KeyEncoder

    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data['email']
        user_id = get_object_or_404(UserProfile, email=user_email).pk

        confirmation_key = self.create_confirmation_key(self.confirmation_key_template) # method from KeyEncoder
        cache.set(confirmation_key, {'user_id': user_id}, timeout=self.timeout) # set key to cache
        self.send_password_reset_link(request, user_email, self.conf_token) # method from RegistrationEmail

        return Response(
            {'message': 'Email sent. Check your mailbox!'},
            status=status.HTTP_204_NO_CONTENT
        )


class ResetPasswordAPIView(mixins.UpdateModelMixin,
                           GenericAPIView):
    """
    View for password reset.
    """
    serializer_class = ResetPasswordSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._object = None

    def get_object(self):
        if self._object is None:
            confirmation_key = settings.PASSWORD_RESET_KEY.format(token=self.kwargs['token'])
            data = cache.get(confirmation_key, {})

            # If there is no link in cache it was expired (or did not exist).
            # Raise TimeoutError anyway.
            if not data:
                raise TimeoutError

            if user_id := data.get('user_id'):
                user = get_object_or_404(UserProfile, pk=user_id)

                # Set user in view cache to avoid multiple sql querying.
                setattr(self, '_object', user)

        return self._object

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.get_object()})
        return context

    def patch(self, request, *args, **kwargs):
        try:
            self.partial_update(request, *args, **kwargs)

            # If not active user tries to reset password, make him active.
            user = self.get_object()
            if not user.is_active:
                user.activate()

            confirmation_key = settings.PASSWORD_RESET_KEY.format(token=self.kwargs['token'])
            cache.delete(confirmation_key)

            return Response(
                {'message': 'Password was changed successfully!'},
                status=status.HTTP_204_NO_CONTENT
            )
        except TimeoutError:
            return Response(
                 {'error': 'Link is expired.'},
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

    # @action(detail=True, methods=['patch'], url_path='set-password')
    # def set_password(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = PasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user.set_password(serializer.validated_data['password'])
    #         user.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
