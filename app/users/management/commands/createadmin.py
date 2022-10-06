from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *arg, **options):
        superuser = User.objects.filter(email="admin@admin.com", is_superuser=True)
        if superuser.count() > 0:
            self.stdout.write("This admin already exists in database!")
        else:
            User.objects.create_superuser(id=1, email="admin@admin.com", password="admin")
            self.stdout.write("Admin created successfully!")
