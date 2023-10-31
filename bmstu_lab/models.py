from django.db import models


# Create your models here.
class Driver(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    driver_license_number = models.CharField(max_length=20)
    issue_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=10, null=True, blank=True)
    status = models.BooleanField()
    url_photo = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'driver'


class Insurance(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    start_date = models.DateField()
    end_date = models.DateField()
    premium_amount = models.FloatField()
    insurance_type = models.BooleanField()
    id_user = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='id_user')
    id_moderator = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='id_moderator', related_name='mod_i')
    status = models.CharField(max_length=20)
    date_create = models.DateField(null=True, blank=True)
    date_form = models.DateField(null=True, blank=True)
    date_over = models.DateField(null=True, blank=True)
    vehicle_make = models.CharField(max_length=50, null=True, blank=True)
    vehicle_model = models.CharField(max_length=50, null=True, blank=True)
    vehicle_year = models.CharField(max_length=4, null=True, blank=True)
    vehicle_vin = models.CharField(max_length=17, null=True, blank=True)
    vehicle_license_plate = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'insurance'


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
