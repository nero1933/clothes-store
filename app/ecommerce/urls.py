from django.urls import path, include

from rest_framework.routers import SimpleRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *
from .views.shopping_carts import ShoppingCartItemViewSet

router = SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='users')
router.register(r'addresses', UserAddressViewSet, basename='addresses')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'shopping_cart_items', ShoppingCartItemViewSet, basename='shopping_cart_items')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/register/user', RegisterUserAPIView.as_view(), name='register_user'),
    path('api/register/guest', RegisterGuestAPIView.as_view(), name='register_guest'),
    path('api/register/confirmation/<str:token>', register_user_confirmation, name='register_user_confirmation'),
    
    path('api/password-reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('api/password-reset/new-password/<str:token>', PasswordResetNewPasswordAPIView.as_view(), name='password_reset_new_password'),

    path('api/', include(router.urls)),
]
