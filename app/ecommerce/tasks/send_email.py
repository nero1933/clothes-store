from celery import shared_task

from django.core.checks import Error
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from django.conf import settings

from ecommerce.models import UserProfile


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
            },
            email = str(email)
        )
    """

    order = context.get('order', None)
    order_id = order.get('id', None)

    print(settings.DEFAULT_FROM_EMAIL)
    print(user_email)

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

    print('END')