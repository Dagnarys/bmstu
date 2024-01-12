import random

from django.core import management
from django.core.management.base import BaseCommand
from insurances.models import *
from .utils import random_date, random_timedelta


def add_drivers():
    Driver.objects.create(
        name="Козлова Елена Михайловна",
        passport_number='9012 345678',
        status=1,
        birth_date='1988-08-10',
        address='ул. Морская, д. 78, кв. 22',
        phone_number='+7 (555) 789-1234',
        email='elena@example.com',
        image="drivers/img1.png"
    )

    Driver.objects.create(
        name="Иванов Иван Иванович",
        passport_number='5678 901234',
        status=1,
        birth_date='1995-02-28',
        address='ул. Примерная, д. 123, кв. 45',
        phone_number='+7 (123) 456-7890',
        email='ivan@example.com',
        image="drivers/img2.png"
    )

    Driver.objects.create(
        name="Петрова Петра Петровна",
        passport_number='2345 678901',
        status=1,
        birth_date='1975-12-20',
        address='ул. Образцовая, д. 45, кв. 12',
        phone_number='+7 (987) 654-3210',
        email='petra@example.com',
        image="drivers/img3.png"
    )

    Driver.objects.create(
        name="Сидоров Алексей Васильевич",
        passport_number='1234 567890',
        status=1,
        birth_date='1980-05-15',
        address='пр. Ленина, д. 34, кв. 7',
        phone_number='+7 (777) 123-4567',
        email='alex@example.com',
        image="drivers/img3.png"
    )

    Driver.objects.create(
        name="Григорьев Дмитрий Николаевич",
        passport_number='2345 678901',
        status=1,
        birth_date='1992-04-03',
        address='пр. Приморский, д. 56, кв. 3',
        phone_number='+7 (111) 987-6543',
        email='dmitry@example.com',
        image="drivers/img5.png"
    )

    print("Услуги добавлены")


def add_insurances():
    users = CustomUser.objects.filter(is_moderator=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(users) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    drivers = Driver.objects.all()

    for _ in range(30):
        insurance = Insurance.objects.create()
        insurance.name = "Страховка №" + str(insurance.pk)
        insurance.status = random.randint(2, 5)

        if insurance.status in [3, 4]:
            if insurance.status == 4:
                insurance.date_complete = None
            else:
                insurance.date_complete = random_date()

            if insurance.date_complete:
                insurance.date_formation = insurance.date_complete - random_timedelta()
            else:
                insurance.date_formation = random_date()

            insurance.date_created = insurance.date_formation - random_timedelta()
            insurance.moderator = random.choice(moderators)
            insurance.premium_amount = 5000+random.randint(0, 10000)
        else:
            insurance.date_formation = random_date()
            insurance.date_created = insurance.date_formation - random_timedelta()

        insurance.employer = random.choice(users)

        for i in range(random.randint(1, 5)):
            insurance.drivers.add(random.choice(drivers))

        insurance.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_drivers()
        add_insurances()