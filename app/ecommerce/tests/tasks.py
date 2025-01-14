from datetime import timedelta

from django.core import mail
from django.utils import timezone
from django.test import TestCase, override_settings

from app import settings

from ecommerce.models import UserProfile
from ecommerce.tasks import delete_old_guest_users
from ecommerce.tasks import send_order_details_email


class DeleteOldGuestUsersTest(TestCase):

    def setUp(self):
        # Create a guest user who logged in more than 24 hours ago
        self.old_guest_user = UserProfile.objects.create(
            email='123',
            is_guest=True,
            last_login=timezone.now() - timedelta(days=2)  # more than a day ago
        )

        # Create a guest user who logged in less than 24 hours ago
        self.recent_guest_user = UserProfile.objects.create(
            email='132',
            is_guest=True,
            last_login=timezone.now() - timedelta(hours=12)  # within the last 24 hours
        )

        # Create a regular (non-guest) user for control purposes
        self.regular_user = UserProfile.objects.create(
            email='231',
            is_guest=False,
            last_login=timezone.now() - timedelta(days=2)  # older login but not a guest
        )

    def test_delete_old_guest_users(self):
        # Ensure that there are 3 users initially
        self.assertEqual(UserProfile.objects.count(), 3)

        # Run the task
        delete_old_guest_users()

        # After running the task, only the old guest user should be deleted
        self.assertFalse(UserProfile.objects.filter(pk=self.old_guest_user.pk).exists(),
                         'Old guest user must be deleted')

        # The recent guest user should still exist
        self.assertTrue(UserProfile.objects.filter(pk=self.recent_guest_user.pk).exists(),
                        'Recent guest user must not be deleted')

        # The regular user should still exist
        self.assertTrue(UserProfile.objects.filter(pk=self.regular_user.pk).exists(),
                        'Regular user must not be deleted')

        # Check that there are now 2 users remaining
        self.assertEqual(UserProfile.objects.count(), 2,
                         'There should be two users left')


class SendOrderDetailsEmailTest(TestCase):
    def setUp(self):
        self.user_email = "test@test.test"
        self.context = {
            "order": {
                "id": "12345",
                "date_created": "2025-01-14",
                "price": "99.99",
            },
            "order_items": [
                ["Product A", "2", "19.99"],
                ["Product B", "1", "59.99"],
            ],
            "shipping_address": {
                "first_name": "John",
                "last_name": "Doe",
                "region": "Region A",
                "street": "123 Main St",
                "unit_number": "Unit 4B",
                "city": "Somewhere",
                "country": "Country",
            },
            "email": self.user_email,
        }

        self.template_path = "ecommerce/order_details.html"

    # @patch("django.core.mail.EmailMultiAlternatives.send")
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_order_details_email(self):
        send_order_details_email(self.user_email, self.context)
        # Check that the email was sent
        self.assertEqual(len(mail.outbox), 1, 'Email must be sent')

        # Get confirmation link from message
        message = mail.outbox[0]

        # """
        # Test that the `send_order_details_email` task sends an email with the correct details.
        # """
        # # Run the task synchronously
        # result = send_order_details_email.apply(args=(self.user_email, self.context))
        #
        # # Assert that the task completed successfully
        # self.assertIsInstance(result, EagerResult)
        # self.assertEqual(result.status, "SUCCESS")
        #
        # # Check if the email was sent
        # mock_send.assert_called_once()
        #
        # # Check the email content
        # message_instance = mock_send.call_args[0][0]

        self.assertIn(f"Order №{self.context['order']['id']}", message.subject)
        self.assertIn(f"Order №{self.context['order']['id']}", message.body)
        self.assertIn(self.context["shipping_address"]["first_name"], message.alternatives[0][0])
        self.assertEqual(message.to, [self.user_email])
        self.assertEqual(message.from_email, settings.DEFAULT_FROM_EMAIL)
