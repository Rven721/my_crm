# Generated by Django 3.0.4 on 2022-09-30 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0038_auto_20220929_1623'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=15, unique=True, verbose_name='Тэг'),
        ),
    ]
