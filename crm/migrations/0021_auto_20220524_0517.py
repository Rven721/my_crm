# Generated by Django 3.0.4 on 2022-05-24 05:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0020_auto_20220522_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(blank=True, default=datetime.time(10, 0), null=True, verbose_name='Время'),
        ),
    ]
