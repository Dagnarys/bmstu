# Generated by Django 4.2.8 on 2023-12-19 13:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0006_alter_insurance_date_created_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='insurance',
            options={'ordering': ('id',), 'verbose_name': 'Страховка', 'verbose_name_plural': 'Страховки'},
        ),
        migrations.AlterField(
            model_name='insurance',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 19, 13, 36, 35, 30156, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 18, 13, 36, 35, 30131, tzinfo=datetime.timezone.utc), verbose_name='Дата конца'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 19, 13, 36, 35, 30117, tzinfo=datetime.timezone.utc), verbose_name='Дата начала'),
        ),
    ]
