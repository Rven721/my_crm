# Generated by Django 3.0.4 on 2022-09-21 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='name_in_dat',
            field=models.CharField(default='dat', max_length=150, verbose_name='Имя в дательном падеже'),
        ),
    ]
