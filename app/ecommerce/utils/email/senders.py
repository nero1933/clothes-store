from rest_framework.reverse import reverse


class ConfirmationEmail:
    """
    Class witch sends emails and receives conformation.
    """
    def _send_confirmation_link(
            self,
            request,
            user_id,
            user_email,
            token,
            reverse_name,
            template,
            subject
    ):
        """
        test.
        """
        confirmation_link = request.build_absolute_uri(
            reverse(reverse_name, kwargs={'token': token})
        )

        print('confirmation_link')
        print(confirmation_link)
        print('confirmation_link')

        # context = {
        #     'confirmation_link': confirmation_link,
        # }
        #
        # html_body = render_to_string(template, context)
        #
        # message = EmailMultiAlternatives(
        #     subject=subject,
        #     body=f'{subject}\n{confirmation_link}',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     to=[user_email]
        # )
        # message.attach_alternative(html_body, "text/html")
        # message.send(fail_silently=False)
        return 1


class RegistrationEmail(ConfirmationEmail):
    """
    test.
    """
    def send_registration_link(self, request, user_id, token, user_email):
        """
        test.
        """
        self._send_confirmation_link(
            request,
            user_id,
            user_email,
            token,
            'register_user_confirmation',
            'ecommerce/register_user_confirmation.html',
            'Confirm registration',
        )


class PasswordResetEmail(ConfirmationEmail):
    """
    test.
    """
    def send_password_reset_link(self, request, user_id, user_email, token):
        self._send_confirmation_link(
            request,
            user_id,
            user_email,
            token,
            'password_reset_new_password',
            'ecommerce/password_reset.html',
            'Password reset',
        )