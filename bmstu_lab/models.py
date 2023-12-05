from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


# Create your models here.


class Driver(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )
    full_name = models.CharField(max_length=255, default="Иванов Иван Иванович", verbose_name="ФИО")
    birth_date = models.DateField(verbose_name="Дата рождения", default="1999-01-01")
    address = models.CharField(max_length=255, default="Москва", verbose_name="Адрес")
    phone_number = models.CharField(max_length=17, default="+7-999-999-99-99", verbose_name="Телефон")
    email = models.CharField(max_length=255, default="asd@gmail.com", verbose_name="Емейл")
    driver_license_number = models.CharField(max_length=20, default="9999 999999", verbose_name="ВУ")
    issue_date = models.DateField(verbose_name="Дата получения", default="2020-05-05")
    expiration_date = models.DateField(verbose_name="Срок действия до", default="2050-05-05")
    passport_number = models.CharField(max_length=11, verbose_name="Паспорт", default="9999 999999")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(upload_to="drivers", default="drivers/img1.png", verbose_name="Фото")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('name', name)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Insurance(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )
    number_insurance = models.CharField(max_length=10, default="xx123xx123", verbose_name="Номер страховки")
    start_date = models.DateField(default=datetime.now(), verbose_name="Дата начала")
    end_date = models.DateField(default=(datetime.now() + timedelta(days=365)), verbose_name="Дата конца")
    premium_amount = models.FloatField(default=0, verbose_name="Сумма")
    insurance_type = models.BooleanField(default=0, verbose_name="Тип страхования")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата создания")
    date_of_formation = models.DateTimeField(null=True, blank=True, verbose_name="Дата формирования")
    date_complete = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")
    vehicle_make = models.CharField(max_length=50, default="", verbose_name="Марка")
    vehicle_model = models.CharField(max_length=50, default="", verbose_name="Модель")
    vehicle_year = models.CharField(max_length=4, default="", verbose_name="Год выпуска")
    vehicle_vin = models.CharField(max_length=17, default="", verbose_name="VIN")
    vehicle_license_plate = models.CharField(max_length=10, default="", verbose_name="Гос. номер")

    drivers = models.ManyToManyField(Driver, verbose_name="Водители", null=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь", null=True)

    def __str__(self):
        return self.number_insurance

    class Meta:
        verbose_name = "Страховка"
        verbose_name_plural = "Страховки"
        ordering = ('-date_of_formation',)
