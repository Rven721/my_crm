# Generated by Django 3.0.4 on 2021-12-28 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='pages',
            field=models.IntegerField(default=1, verbose_name='Число страниц'),
        ),
    ]