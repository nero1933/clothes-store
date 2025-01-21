from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings


@shared_task
def send_order_details_email(user_email, context):
    """
    Sends order details email to user's email

    :param user_email str(email)
    :param context
        dict(
            order={
                'id': 'id',
                'date_created': 'date_created',
                'price': 'price',
            },
            order_items=[['name', 'quantity', 'price'], ],
            shipping_address={
                'first_name': 'first_name',
                'last_name': 'last_name',
                'region': 'region',
                'street': 'street',
                'unit_number': 'unit_number',
                'city': 'city',
                'country': 'country',
                'phone_number': 'phone_number',
            },
            email = str(email)
        )
    """

    order = context.get('order', None)
    order_id = order.get('id', None)

    template = 'ecommerce/order_details.html'
    html_body = render_to_string(template, context)
    message = EmailMultiAlternatives(
        subject=f"Order №{order_id}",
        body=f"Order №{order_id}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email]
    )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)
