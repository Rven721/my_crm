# Generated by Django 3.0.4 on 2022-09-21 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='name_in_dat',
            field=models.CharField(default='<django.db.models.fields.CharField>_dat', max_length=30, verbose_name='Имя в дательном падеже'),
        ),
    ]
