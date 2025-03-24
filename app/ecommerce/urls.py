from django.urls import path, include

from rest_framework.routers import SimpleRouter

from rest_framework_simplejwt.views import TokenObtainPairView

from .views import *
from .views.payments import CreateCheckoutSessionAPIView, StripeWebhookView
from .views.reviews import ReviewViewSet
from .views.shopping_carts import ShoppingCartItemViewSet

router = SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='users')
router.register(r'addresses', UserAddressViewSet, basename='addresses')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'shopping_cart_items', ShoppingCartItemViewSet, basename='shopping_cart_items')
router.register(r'orders', OrderViewSet, basename='orders')

router2 = SimpleRouter()
router2.register(
    r'orders/(?P<order_id>\d+)/'
    r'order_items/(?P<order_item_id>\d+)/'
    r'products/(?P<product_slug>[^/.]+)/'
    r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/logout/', LogoutView.as_view(), name='logout'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # delete & change create guest
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/register/user/', RegisterUserAPIView.as_view(), name='register_user'),
    path('api/v1/register/guest/', RegisterGuestAPIView.as_view(), name='register_guest'),
    path('api/v1/register/confirmation/<str:token>/', register_user_confirmation, name='register_user_confirmation'),

    path('api/v1/password-reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('api/v1/password-reset/new-password/<str:token>/', PasswordResetNewPasswordAPIView.as_view(),
         name='password_reset_new_password'),

    path('api/v1/create-order/user/', OrderUserCreateAPIView.as_view(), name='create_order_user'),
    path('api/v1/create-order/guest/', OrderGuestCreateAPIView.as_view(), name='create_order_guest'),
    #
    path('api/v1/payment/<int:order_id>/checkout/', CreateCheckoutSessionAPIView.as_view(), name='payment_checkout'),
    # path('api/v1/payment/<int:?>/successful/', '#', name='payment_successful'),
    # path('api/v1/payment/<int:?>/cancelled/', '#', name='payment_cancelled'),
    path('api/v1/stripe_webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),

    path('api/v1/'
         'orders/<int:order_id>/'
         'order_items/<int:order_item_id>/'
         'products/<str:product_slug>/'
         'reviews/',
         ReviewViewSet.as_view({'post': 'create'}),
         name='reviews_create'),
    path('api/v1/'
         'orders/<int:order_id>/'
         'order_items/<int:order_item_id>/'
         'products/<str:product_slug>/'
         'reviews/<int:pk>/',
         ReviewViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}),
         name='reviews_rud'),

    path('api/v1/', include(router.urls)),
    # path('api/v1/', '#', name='#'),

    #path('api/v1/<order_id>', TempPaymentClass.as_view(), name='temp_order'),
]
