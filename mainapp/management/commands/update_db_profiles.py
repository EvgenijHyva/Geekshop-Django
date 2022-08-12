from django.core.management.base import BaseCommand
from authapp.models import ShopUserProfile, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            user_profile, new_profile = ShopUserProfile.objects.get_or_create(user=user)
            if new_profile:
                print(f"created profile for {user_profile}")