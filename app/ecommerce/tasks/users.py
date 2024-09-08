from datetime import timedelta

from django.utils import timezone

from celery import shared_task


@shared_task
def delete_old_guest_users():
    from ecommerce.models import UserProfile
    # Calculate the threshold datetime (24 hours ago)
    threshold_time = timezone.now() - timedelta(days=1)

    # Filter for guest users who last logged in more than a day ago
    old_guest_users = UserProfile.objects.filter(is_guest=True, last_login__lt=threshold_time)

    # Count and delete these users
    count, _ = old_guest_users.delete()

    # Optionally, log how many users were deleted
    # print(f'Deleted {count} guest users who logged in more than a day ago.')
