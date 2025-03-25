from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

from app import settings
from ecommerce.utils.confirmation_managers.confirmation_managers import ConfirmationCacheManager


class SendEmail:
    """
    test
    """

    from_email = settings.DEFAULT_FROM_EMAIL

    def send_email(
            self,
            user_email: str,
            subject: str,
            text_template: str,
            text_context: dict,
            html_template: str,
            html_context: dict,
    ):
        """
        test
        """

        text_content = render_to_string(text_template, text_context)
        html_content = render_to_string(html_template, html_context)

        email = EmailMultiAlternatives(
            subject,
            text_content,
            self.from_email,
            [user_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()


class ConfirmationEmail(SendEmail, ConfirmationCacheManager):
    """
    test
    """

    subject: str
    text_template: str
    html_template: str
    path: str
    confirmation_key_template: str
    confirmation_flag_template: str
    timeout: int

    frontend_url = settings.FRONTEND_URL

    # def __init__(self):
    #     super().__init__()
    #     ConfirmationCacheManager.__init__(self)
    #     self.frontend_url = settings.FRONTEND_URL

    def create_confirmation_url(self, path: str):
        """
        :param path: must end with /
        :return: confirmation_url
        """

        # must end with slash '/'
        confirmation_url = f'{self.frontend_url}{path}{self.conf_token}/'
        return confirmation_url

    def send_confirmation_email(
            self,
            user_email: str,
            subject: str,
            text_template: str,
            html_template: str,
            path: str,
    ) -> None:

        # if self.confirmation_flag:
        #     raise ValidationError("A valid confirmation email has already been sent.")

        if not self.conf_token:
            raise Exception("Failed send confirmation email, no 'conf_token'!")

        confirmation_url = self.create_confirmation_url(path)
        text_context = html_context = {'confirmation_url': confirmation_url}

        self.send_email(
            user_email,
            subject,
            text_template,
            text_context,
            html_template,
            html_context
        )

    def prepare_and_send_confirmation_email(self, user_email: str, user_id: int) -> None:
        """
        Caches confirmation data and sends a confirmation email.
        """

        # Step 1: Cache the confirmation data

        # Function form ConfirmationCacheManager
        # Creates confirmation_key and confirmation_flag
        # Sets them to cache.
        # Key contains token which would be sent
        # to user in email as a part of url.
        # Url leads to account activation page.
        # Flag is used to monitor if key is still in cache.
        # Value of key is {'user_id': user_id} (dict)
        # Value of flag is True (bool)

        self.cache_confirmation_data(
            self.confirmation_key_template,
            self.confirmation_flag_template,
            user_id,
            self.timeout,
            store_flag=True,
        )

        # Step 2: Send the email
        confirmation_url = self.create_confirmation_url(self.path)
        text_context = html_context = {'confirmation_url': confirmation_url}

        self.send_email(
            user_email=user_email,
            subject=self.subject,
            text_template=self.text_template,
            text_context=text_context,
            html_template=self.html_template,
            html_context=html_context,
        )

class ActivationEmail(ConfirmationEmail):
    """
    Handles sending activation emails.
    """

    subject = "Activate your account"
    text_template = "ecommerce/confirm_registration.txt"
    html_template = "ecommerce/confirm_registration.html"
    frontend_path = "activate/"

    confirmation_key_template = settings.USER_CONFIRMATION_KEY_TEMPLATE
    confirmation_flag_template = settings.USER_CONFIRMATION_FLAG_TEMPLATE
    timeout = settings.USER_CONFIRMATION_TIMEOUT


class PasswordResetEmail(ConfirmationEmail):
    """
    Handles sending password reset emails.
    """

    subject = "Reset your password"
    text_template = "emails/password_reset_email.txt"
    html_template = "emails/password_reset_email.html"
    frontend_path = "reset-password/"

    confirmation_key_template = settings.USER_CONFIRMATION_KEY_TEMPLATE
    confirmation_flag_template = settings.USER_CONFIRMATION_FLAG_TEMPLATE
    timeout = settings.USER_CONFIRMATION_TIMEOUT
