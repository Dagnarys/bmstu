# Generated by Django 4.2.8 on 2023-12-19 14:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu_lab', '0007_alter_insurance_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 19, 14, 53, 7, 962188, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 18, 17, 53, 7, 962154), verbose_name='Дата конца'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 19, 17, 53, 7, 962141), verbose_name='Дата начала'),
        ),
    ]