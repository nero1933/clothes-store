from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from ecommerce.models import UserProfile
from ecommerce.tasks import delete_old_guest_users


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
        pass

    def test_send_order_details_email(self):
        pass
