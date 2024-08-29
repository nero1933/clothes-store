from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from app import settings


@shared_task
def send_order_email(user_email, context):
    template = 'ecommerce/order_details.html'

    html_body = render_to_string(template, context)

    text_body = strip_tags(html_body)

    message = EmailMultiAlternatives(
        subject=f"Order №{context.get('order_id')}",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email]
    )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)