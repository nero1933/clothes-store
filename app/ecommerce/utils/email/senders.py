# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from app import settings
#
#
# class ConfirmationEmail:
#     """
#     Class witch sends emails and receives conformation.
#     """
#     def _send_confirmation_link(
#             self,
#             request,
#             user_email,
#             token,
#             reverse_name,
#             template,
#             subject
#     ):
#         """
#         tests.
#         """
#         # confirmation_link = request.build_absolute_uri(
#         #     reverse(reverse_name, kwargs={'token': token})
#         # )
#         path = ''
#
#         if reverse_name == 'register_user_confirmation':
#             path = 'activate'
#         elif reverse_name == 'reset_password':
#             path = 'reset-password'
#
#         """ TEMP !!! """
#         confirmation_link = f'http://localhost:3000/{path}/{token}'
#
#         context = {
#             'confirmation_link': confirmation_link,
#         }
#
#         html_body = render_to_string(template, context)
#
#         message = EmailMultiAlternatives(
#             subject=subject,
#             body=f'{subject}\n{confirmation_link}',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[user_email]
#         )
#         message.attach_alternative(html_body, "text/html")
#         message.send(fail_silently=False)
#
#
# class RegistrationEmail(ConfirmationEmail):
#     """
#     tests.
#     """
#     def send_registration_link(self, request, user_email, token):
#         """
#         tests.
#         """
#         self._send_confirmation_link(
#             request,
#             user_email,
#             token,
#             'register_user_confirmation',
#             'ecommerce/confirm_registration.html',
#             'Confirm registration',
#         )
#
#
# class PasswordResetEmail(ConfirmationEmail):
#     """
#     tests.
#     """
#     def send_password_reset_link(self, request, user_email, token):
#         """
#         tests.
#         """
#         self._send_confirmation_link(
#             request,
#             user_email,
#             token,
#             'reset_password',
#             'ecommerce/reset_password.html',
#             'Password reset',
#         )