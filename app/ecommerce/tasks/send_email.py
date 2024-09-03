from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from app import settings


@shared_task
def send_order_email(user_email, context):
    """ Sends order detail email to user's email """

    template = 'ecommerce/order_details.html'
    html_body = render_to_string(template, context)
    message = EmailMultiAlternatives(
        subject=f"Order №{context.get('order_id', None)}",
        body=f"Order №{context.get('order_id', None)}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email]
    )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)