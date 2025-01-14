from django.core.management.base import BaseCommand

from ecommerce.models import UserProfile


class Command(BaseCommand):
    help = 'Creates superuser. Used in developing and testing.'

    def handle(self, *args, **options):
        try:
            user = UserProfile.objects.create_superuser(
                email='test@test.test',
                first_name='R',
                last_name='N',
                phone=None,
                password='123456789',
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser {user.email}'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
