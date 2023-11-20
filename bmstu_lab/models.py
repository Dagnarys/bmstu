from datetime import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class Driver(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )
    full_name = models.CharField(max_length=255, default="Иванов Иван Иванович", verbose_name="ФИО")
    birth_date = models.DateField()
    address = models.CharField(max_length=255,default="Москва",  verbose_name="Адрес")
    phone_number = models.CharField(max_length=17, default="+7-999-999-99-99",  verbose_name="Телефон")
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


class Insurance(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата конца")
    premium_amount = models.FloatField(default=9999.99,verbose_name="Сумма")
    insurance_type = models.BooleanField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_create = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата создания")
    date_form = models.DateTimeField(null=True, blank=True, verbose_name="Дата формирования")
    date_over = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")
    vehicle_make = models.CharField(max_length=50, verbose_name="Марка")
    vehicle_model = models.CharField(max_length=50, verbose_name="Модель")
    vehicle_year = models.CharField(max_length=4, verbose_name="Год выпуска")
    vehicle_vin = models.CharField(max_length=17, verbose_name="VIN")
    vehicle_license_plate = models.CharField(max_length=10, verbose_name="Гос. номер")

    drivers = models.ManyToManyField(Driver, verbose_name="Водители", null=True)

    def __str__(self):
        return self.vehicle_vin

    class Meta:
        verbose_name = "Страховка"
        verbose_name_plural = "Страховки"


class Users(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    admin = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users'


class DriverInsurance(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    id_driver = models.ForeignKey(Driver, on_delete=models.CASCADE, db_column='id_driver')
    id_insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, db_column='id_insurance')

    class Meta:
        managed = False
        db_table = 'driver_insurance'
