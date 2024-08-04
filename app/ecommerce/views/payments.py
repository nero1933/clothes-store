import stripe
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from ecommerce.models import Order
from ecommerce.serializers.payments import CreateCheckoutSessionSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionAPIView(APIView):
    #
    # Create OrderReadOnlyViewSet
    # Create Order tests
    # Make checkout session achievable by order_id (in urls.py <int:order_id>)
    # Make command to create stripe.Products # https://docs.stripe.com/api/products
    # Make command to create stripe.Price # https://docs.stripe.com/api/prices
    # Make signal to change stripe.Price if product_item.price is changed (if it is possible)
    # Make signal to create Payment when new order is created
    # Make Order -> to -> stripe.checkout.Session method
    # Make proper webhook handlers for every event
    #    Make payment successful handler. Set payment.stripe_id

    def get_queryset(self):
        queryset = Order.objects \
            .prefetch_related('order_item') \
            .select_related('order_item__product_variation__product_item') \
            .filter(user=self.request.user)

        return queryset

    def post(self, request):
        serializer = CreateCheckoutSessionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': serializer.validated_data['currency'],
                            'product_data': {
                                'name': 'T-shirt',
                            },
                            'unit_amount': serializer.validated_data['amount'],
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=settings.REDIRECT_DOMAIN + '/api/v1/payments/checkout/success', # BAD CODE
                    cancel_url=serializer.validated_data['cancel_url'],
                )
                return Response({'id': session.id, 'url': session.url})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StripeWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            # Invalid payload
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            self.handle_checkout_session(session)

        # Add additional event types as needed

        return Response(status=status.HTTP_200_OK)

    def handle_checkout_session(self, session):
        # Get id session. Set it to payments

        # Fulfill the purchase or update order status
        print("Payment was successful.")
        print(session)