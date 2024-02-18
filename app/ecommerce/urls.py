from django.urls import path, include

from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/register/', RegisterUserAPIView.as_view(), name='register_user'),
    path('api/register/confirmation/<str:token>', confirm_register_user, name='register_user_confirmation'),
]