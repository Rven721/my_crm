# Generated by Django 3.0.4 on 2021-12-28 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_auto_20211228_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='took_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='Затраченное время в секундах'),
        ),
    ]