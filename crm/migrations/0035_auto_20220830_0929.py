# Generated by Django 3.0.4 on 2022-08-30 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0034_auto_20220624_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='took_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='Затраченное время'),
        ),
    ]