from django.core.management.base import BaseCommand
from insurances.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Driver.objects.all().delete()
        Insurance.objects.all().delete()
        CustomUser.objects.all().delete()
