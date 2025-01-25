import stripe

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.core.exceptions import BadRequest

from ecommerce.models import Order, OrderItem
from ecommerce.models.payments import Payment
from ecommerce.tasks.send_email import send_order_details_email

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, order_id):
        user_filter = {'order__user': self.request.user} \
            if not self.request.user.is_guest \
            else {'order__guest': self.request.user}

        queryset = OrderItem.objects \
            .select_related('order', 'product_variation__product_item') \
            .only('id', 'order__id', 'quantity', 'product_variation__product_item__stripe_price_id') \
            .filter(**user_filter, order_id=order_id)

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

    def create_checkout_session(self, order_id):
        line_items = self.get_line_items(order_id)
        if not line_items:
            raise BadRequest('No order items available')

        # success_link = self.request.build_absolute_uri(reverse('orders-detail', kwargs={'pk': order_id}))
        success_link = 'https://google.com'
        cancel_url = 'https://google.com'

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_link,
            cancel_url=cancel_url,
        )

        return checkout_session

    def post(self, request, order_id, *args, **kwargs):
        payment = get_object_or_404(Payment, order=order_id)
        if payment.payment_bool:
            return Response('Order is paid', status=status.HTTP_400_BAD_REQUEST)

        if payment.stripe_session_id:
            return Response('Checkout session already exists', status=status.HTTP_400_BAD_REQUEST)

        checkout_session = self.create_checkout_session(order_id)
        payment.stripe_session_id = checkout_session.id
        payment.save()

        return Response({'checkout_session_id': checkout_session.id,
                         'checkout_session_url': checkout_session.url},
                        status=status.HTTP_201_CREATED)

    def get(self, request, order_id, *args, **kwargs):
        payment = get_object_or_404(Payment, order=order_id)
        if payment.payment_bool:
            return Response('Order is paid', status=status.HTTP_400_BAD_REQUEST)

        if not payment.stripe_session_id:
            return Response('Checkout session does not exists', status=status.HTTP_400_BAD_REQUEST)

        checkout_session = stripe.checkout.Session.retrieve(payment.stripe_session_id)
        if checkout_session.status == 'expired':
            return Response('Checkout session is expired', status=status.HTTP_400_BAD_REQUEST)

        return Response({'checkout_session_id': checkout_session.id,
                         'checkout_session_url': checkout_session.url},
                        status=status.HTTP_200_OK)


class StripeWebhookView(APIView):

    def get_queryset(self, order_id):
        queryset = OrderItem.objects \
            .select_related(
                'product_variation__product_item__product',
                'order__shipping_address'
            ) \
            .filter(order_id=order_id) \
            .only(
                'id', 'order_id', 'product_variation_id', 'quantity', 'price',
                'order__date_created', 'order__order_price', 'order__user_id', 'order__shipping_address',
                'product_variation__product_item_id', 'product_variation__product_item__product_id',
                'product_variation__product_item__price', 'product_variation__product_item__product__name',
            )

        return queryset

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
            self.handle_completed_session(session)
        if event['type'] == 'checkout.session.expired':
            session = event['data']['object']
            self.handle_expired_session(session)
            return Response('Checkout session is expired. Create a new one', status=status.HTTP_400_BAD_REQUEST)
        # if event['type'] == 'payment_intent.succeeded':
        #     session = event['data']['object']
        #     self.handle_payment_intent(session)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def handle_completed_session(self, session):

        payment = get_object_or_404(
            Payment.objects.select_related('order') \
                .only('id', 'order_id', 'payment_bool', 'stripe_session_id', 'order__order_status'),
            stripe_session_id=session.id
        )

        payment.payment_bool = True
        payment.order.order_status = 2 # PAYED
        payment.save()
        payment.order.save()

        context = self.get_order_email_context(payment.order.id)
        user_email = context.pop('email', None)

        send_order_details_email.delay(user_email, context)  # Celery task

    def handle_expired_session(self, session):
        payment = get_object_or_404(Payment, stripe_session_id=session.id)

        payment.stripe_session_id = ''
        payment.save()

    def get_order_email_context(self, order_id) -> (str, list):
        """

        :return: email, context
        """
        queryset = self.get_queryset(order_id)

        if not queryset:
            return None

        order_obj = queryset[0].order
        order = {
            'id': order_obj.pk,
            'date_created': order_obj.date_created.date(),
            'price': order_obj.order_price / 100,
        }
        shipping_address_obj = order_obj.shipping_address

        shipping_address = {
            'first_name': shipping_address_obj.first_name,
            'last_name': shipping_address_obj.last_name,
            'region': shipping_address_obj.region,
            'street': shipping_address_obj.street,
            'unit_number': shipping_address_obj.unit_number,
            'city': shipping_address_obj.city,
            'country': shipping_address_obj.country,
            'phone_number': str(shipping_address_obj.phone_number),
        }

        order_items = [[x.product_variation.product_item.product.name, x.quantity, x.price / 100] for x in queryset]
        email = order_obj.user.email

        context = dict(
            order=order,
            order_items=order_items,
            shipping_address=shipping_address,
            email=email,
        )

        return context
