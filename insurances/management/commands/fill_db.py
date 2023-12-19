import random

from django.core import management
from django.core.management.base import BaseCommand
from insurances.models import *
from .utils import random_date, random_timedelta


def add_drivers():
    Driver(
        full_name='Козлова Елена Михайловна',
        birth_date='1992-04-03',
        address='ул. Морская, д. 78, кв. 22',
        phone_number='+7 (555) 789-1234',
        email='elena@example.com',
        driver_license_number='GH567890',
        issue_date='2017-09-18',
        expiration_date='2027-09-18',
        passport_number='2345 678901'
    ).save()

    Driver(
        full_name='Иванов Иван Иванович',
        birth_date='1980-05-15',
        address='ул. Примерная, д. 123, кв. 45',
        phone_number='+7 (123) 456-7890',
        email='ivan@example.com',
        driver_license_number='AB123456',
        issue_date='2005-07-20',
        expiration_date='2030-07-20',
        passport_number='1234 567890'
    ).save()

    Driver(
        full_name='Петрова Петра Петровна',
        birth_date='1995-02-28',
        address='ул. Образцовая, д. 45, кв. 12',
        phone_number='+7 (987) 654-3210',
        email='petra@example.com',
        driver_license_number='CD789012',
        issue_date='2018-11-10',
        expiration_date='2028-11-10',
        passport_number='5678 901234',
    )

    Driver(
        full_name='Сидоров Алексей Васильевич',
        birth_date='1988-08-10',
        address='пр. Приморский, д. 56, кв. 3',
        phone_number='+7 (777) 123-4567',
        email='alex@example.com',
        driver_license_number='EF345678',
        issue_date='2010-03-05',
        expiration_date='2030-03-05',
        passport_number='9012 345678',

    )

    Driver(
        full_name='Григорьев Дмитрий Николаевич',
        birth_date='1975-12-20',
        address='пр. Ленина, д. 34, кв. 7',
        phone_number='+7 (111) 987-6543',
        email='dmitry@example.com',
        driver_license_number='IJ123456',
        issue_date='2002-06-12',
        expiration_date='2032-06-12',
        passport_number='6789 012345',
    )

    print("Услуги добавлены")


def add_insurances():
    users = CustomUser.objects.filter(is_moderator=False)
    if len(users) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    drivers = Driver.objects.all()

    for _ in range(10):
        insurance = Insurance.objects.create()
        insurance.name = "Страховка №" + str(insurance.pk)
        insurance.status = random.randint(2, 5)

        if insurance.status in [3, 4]:
            insurance.date_complete = random_date()
            insurance.date_of_formation = insurance.date_complete - random_timedelta()
            insurance.date_created = insurance.date_of_formation - random_timedelta()
        else:
            insurance.date_of_formation = random_date()
            insurance.date_created = insurance.date_of_formation - random_timedelta()

        insurance.user = random.choice(users)

        for i in range(random.randint(1, 5)):
            insurance.drivers.add(random.choice(drivers))

        insurance.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # management.call_command("clean_db")

        add_drivers()
        add_insurances()
