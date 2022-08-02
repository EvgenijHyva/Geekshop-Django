from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        model = get_user_model()
        if not model.objects.filter(username="django"):
            django = model.objects.create_superuser(username="django", email="django@local.base")
            django.set_password("geekbrains")
            django.save()
        else:
            print("django already exists")