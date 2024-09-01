from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from app import settings


@shared_task
def send_order_email(user_email, context):
    template = 'ecommerce/order_details.html'

    html_body = render_to_string(template, context)

    # text_body = strip_tags(html_body)

    print(settings.DEFAULT_FROM_EMAIL)

    message = EmailMultiAlternatives(
        subject=f"Order №{context.get('order_id')}",
        body=f"Order №{context.get('order_id')}",
        from_email='nero.pet.1933@gmail.com',
        to=[user_email]
    )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)