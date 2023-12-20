# Generated by Django 4.2.8 on 2023-12-20 07:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0002_alter_insurance_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 20, 7, 55, 59, 371847, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 19, 7, 55, 59, 371822, tzinfo=datetime.timezone.utc), verbose_name='Дата конца'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 20, 7, 55, 59, 371809, tzinfo=datetime.timezone.utc), verbose_name='Дата начала'),
        ),
    ]
