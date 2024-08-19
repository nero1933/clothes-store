from django.urls import path, include

from rest_framework.routers import SimpleRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *
from .views.payments import CreateCheckoutSessionAPIView, StripeWebhookView
from .views.shopping_carts import ShoppingCartItemViewSet

router = SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='users')
router.register(r'addresses', UserAddressViewSet, basename='addresses')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'shopping_cart_items', ShoppingCartItemViewSet, basename='shopping_cart_items')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/register/user/', RegisterUserAPIView.as_view(), name='register_user'),
    path('api/v1/register/guest/', RegisterGuestAPIView.as_view(), name='register_guest'),
    path('api/v1/register/confirmation/<str:token>', register_user_confirmation, name='register_user_confirmation'),

    path('api/v1/create_order/', OrderCreateAPIView.as_view(), name='create_order'),
    #
    path('api/v1/payment/checkout/<int:order_id>', CreateCheckoutSessionAPIView.as_view(), name='payment_checkout'),
    # path('api/v1/payment/successful/', '#', name='payment_successful'),
    # path('api/v1/payment/cancelled/', '#', name='payment_cancelled'),
    path('api/v1/stripe_webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),


    path('api/v1/password-reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('api/v1/password-reset/new-password/<str:token>/', PasswordResetNewPasswordAPIView.as_view(), name='password_reset_new_password'),

    path('api/v1/', include(router.urls)),
    # path('api/v1/', '#', name='#'),
]
