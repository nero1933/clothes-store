import stripe
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from ecommerce.models import Order, OrderItem
from ecommerce.models.payments import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, order_id):
        queryset = OrderItem.objects \
            .select_related('order', 'product_variation__product_item') \
            .prefetch_related('order__payment') \
            .filter(order__user=self.request.user, order_id=order_id)

        return queryset

    def get_line_items(self, order_id: Order.pk) -> []:
        """
        Method takes an order_id, extracts stripe_price_id and quantity
        for every ordered item in the order,
        returns them as a list of dictionaries.

        :param order_id: Order.id
        :return: [{'price': str, 'quantity': int}]
        """
        queryset = self.get_queryset(order_id)

        line_items = []
        for order_item in queryset:
            price_id = order_item.product_variation.product_item.stripe_price_id
            quantity = order_item.quantity
            line_items.append({'price': price_id, 'quantity': quantity})

        return line_items

    def post(self, request, order_id):
        payment = get_object_or_404(Payment, order=order_id)
        # payment = Payment.objects.get(order=order_id)
        if payment.payment_bool:
            return Response('Order is paid', status=status.HTTP_400_BAD_REQUEST)

        line_items = self.get_line_items(order_id)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://google.com',
            cancel_url='https://google.com',
        )
        payment.stripe_session_id = session.id
        payment.save()
        return Response({'checkout_session_id': session.id,
                         'checkout_session_url': session.url},
                        status=status.HTTP_200_OK)


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
        # if event['type'] == 'payment_intent.succeeded':
        #     session = event['data']['object']
        #     self.handle_payment_intent(session)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def handle_checkout_session(self, session):
        payment = get_object_or_404(Payment, stripe_session_id=session.id)
        # payment = Payment.objects.get(stripe_session_id=session.id)
        if payment:
            payment.payment_bool = True
            payment.save()

        # SEND EMAIL
        # ORDER PAID