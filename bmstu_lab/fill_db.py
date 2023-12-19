from django.core.management import BaseCommand

from bmstu_lab.models import Users


def add_users():
    Users.objects.create_user("user1", "user1@user.com", "1234")
    Users.objects.create_superuser("root", "root@root.com", "1234")

    print("Пользователи созданы")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()