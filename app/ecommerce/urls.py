from django.urls import path, include

from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/users/register/', RegisterUserAPIView.as_view(), name='register_user'),
    path('api/users/register/confirmation/<str:token>', register_user_confirmation, name='register_user_confirmation'),
    
    path('api/users/password-reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('api/users/password-reset/new-password/<str:token>', PasswordResetNewPasswordAPIView.as_view(), name='password_reset_new_password'),
]
