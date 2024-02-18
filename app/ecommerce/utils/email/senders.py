import uuid

from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework.reverse import reverse

from app import settings


class SendConfirmationEmail:
    """
    Class witch sends emails and receives conformation.
    """
    def _send_confirmation_link(self, request, user_id, user_email, reverse_name, template, subject):
        """
        test.
        """
        token = uuid.uuid4().hex
        confirmation_key = settings.USER_CONFIRMATION_KEY.format(token=token)
        cache.set(confirmation_key, {'user_id': user_id}, timeout=settings.USER_CONFIRMATION_TIMEOUT)

        confirmation_link = request.build_absolute_uri(
            reverse(reverse_name, kwargs={'token': token})
        )

        print('-----------')
        print(confirmation_link)
        print('-----------')

        context = {
            'confirmation_link': confirmation_link,
        }

        html_body = render_to_string(template, context)

        message = EmailMultiAlternatives(
            subject=subject,
            body=f'{subject}\n{confirmation_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email]
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)


class SendRegistrationEmail(SendConfirmationEmail):
    """
    test.
    """
    def send_registration_link(self, request, user_id, user_email):
        """
        test.
        """
        self._send_confirmation_link(
            request,
            user_id,
            user_email,
            'register_user_confirmation',
            'ecommerce/register_user_confirmation.html',
            'Confirm registration',
        )