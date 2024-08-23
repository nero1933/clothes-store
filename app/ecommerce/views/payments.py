import stripe

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from ecommerce.models import Order, OrderItem
from ecommerce.models.payments import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionAPIView(APIView):
    #
    # Create OrderReadOnlyViewSet (DONE!)
    # Create Order tests (DONE!)
    # Make command to create stripe.Products # https://docs.stripe.com/api/products (DONE!)
    # Make command to create stripe.Price # https://docs.stripe.com/api/prices (DONE!)
    # Make signal to change stripe.Price if product_item.price is changed (DONE!)
    # Make signal to create Payment when new order is created (DONE!)
    # Make Order -> to -> stripe.checkout.Session method
    # Make proper webhook handlers for every event
    # ---- Make payment successful handler. Set payment.stripe_id

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
        line_items = self.get_line_items(order_id)
        payment = Payment.objects.get(order=order_id)
        if not payment.payment_bool:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='https://google.com',
            )
            payment.stripe_session_id = session.id
            payment.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Order is payed', status=status.HTTP_400_BAD_REQUEST)

        # serializer = CreateCheckoutSessionSerializer(data=request.data)
        # if serializer.is_valid():


            # Create get all order_items method

        #     try:
        #
        #         # Create order_to_checkout_session method
        #
        #         session = stripe.checkout.Session.create( # https://docs.stripe.com/api/checkout/sessions/object
        #             payment_method_types=['card'],
        #             line_items=[{
        #                 'price_data': {
        #                     'currency': serializer.validated_data['currency'],
        #                     'product_data': {
        #                         'name': 'T-shirt',
        #                     },
        #                     'unit_amount': serializer.validated_data['amount'],
        #                 },
        #                 'quantity': 1,
        #             }],
        #             mode='payment',
        #             # success_url=settings.REDIRECT_DOMAIN + '/api/v1/payment/checkout/success', # BAD CODE
        #             success_url='127.0.0.1:8000/api/v1/payment/checkout/success',  # BAD CODE
        #             cancel_url='127.0.0.1:8000/api/v1/payment/checkout/cancel',  # BAD CODE
        #         )
        #         return Response({'id': session.id, 'url': session.url, 'order_id': order_id})
        #     except Exception as e:
        #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        #
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        #     self.handle_checkout_session(session)

        return Response('msg', status=status.HTTP_200_OK)

    def handle_checkout_session(self, session):
        payment = Payment.objects.get(stripe_session_id=session.id)
        if payment:
            payment.payment_bool = True
            payment.save()