from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from app import settings

from ecommerce.utils.confirmation_managers.confirmation_managers import ConfirmationCacheManager


class EcommerceEmail:
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
        email.send(fail_silently=False)


class ConfirmationEmail(EcommerceEmail, ConfirmationCacheManager):
    """
    test
    """

    subject: str
    text_template: str
    html_template: str
    frontend_path: str
    confirmation_key_template: str
    confirmation_counter_template: str
    timeout: int

    frontend_url = settings.FRONTEND_URL

    def create_confirmation_url(self, frontend_path: str):
        """
        :param frontend_path: must end with /
        :return: confirmation_url
        """

        # must end with slash '/'
        confirmation_url = f'{self.frontend_url}{frontend_path}{self.conf_token}/'
        return confirmation_url

    def send_confirmation_email(
            self,
            user_email: str,
            subject: str,
            text_template: str,
            html_template: str,
            frontend_path: str,
    ) -> None:

        # if self.confirmation_flag:
        #     raise ValidationError("A valid confirmation email has already been sent.")

        if not self.conf_token:
            raise Exception("Failed send confirmation email, no 'conf_token'!")

        confirmation_url = self.create_confirmation_url(frontend_path)
        text_context = html_context = {'confirmation_url': confirmation_url}

        self.send_email(
            user_email,
            subject,
            text_template,
            text_context,
            html_template,
            html_context
        )

    def prepare_and_send_confirmation_email(self, user_id: int, user_email: str) -> None:
        """
        Caches confirmation data and sends a confirmation email.
        """

        # Step 1: Cache the confirmation data
        self.handle_cache_confirmation(user_id)

        # Step 2: Send confirmation email
        self.send_confirmation_email(
            user_email=user_email,
            subject=self.subject,
            text_template=self.text_template,
            html_template=self.html_template,
            frontend_path=self.frontend_path,
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
    timeout_key = settings.USER_CONFIRMATION_KEY_TIMEOUT

    confirmation_counter_template = settings.USER_CONFIRMATION_COUNTER_TEMPLATE
    timeout_counter = settings.USER_CONFIRMATION_COUNTER_TIMEOUT

    max_attempts = settings.USER_CONFIRMATION_MAX_ATTEMPTS


class ForgotPasswordEmail(ConfirmationEmail):
    """
    Handles sending password reset emails.
    """

    subject = "Reset your password"
    text_template = "ecommerce/reset_password.txt"
    html_template = "ecommerce/reset_password.html"
    frontend_path = "reset-password/"

    confirmation_key_template = settings.RESET_PASSWORD_KEY_TEMPLATE
    timeout_key = settings.RESET_PASSWORD_KEY_TIMEOUT

    confirmation_counter_template = settings.RESET_PASSWORD_COUNTER_TEMPLATE
    timeout_counter = settings.RESET_PASSWORD_COUNTER_TIMEOUT

    max_attempts = settings.RESET_PASSWORD_MAX_ATTEMPTS
