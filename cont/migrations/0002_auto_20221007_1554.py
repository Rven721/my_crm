# Generated by Django 3.0.4 on 2022-10-07 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cont', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'verbose_name': 'Контракт', 'verbose_name_plural': 'Контракты'},
        ),
        migrations.AlterModelOptions(
            name='statuschangelog',
            options={'verbose_name': 'Смена статусов', 'verbose_name_plural': 'Смены статусов'},
        ),
        migrations.RenameField(
            model_name='contract',
            old_name='projct',
            new_name='project',
        ),
        migrations.AlterField(
            model_name='contract',
            name='number',
            field=models.CharField(max_length=20, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='payment_stauts',
            field=models.CharField(choices=[('first_pay_wait', 'Платеж 1 ожидание'), ('second_pay_receive', 'Платеж 1 пулучен'), ('second_pay_wait', 'Платеж 2 ожидание'), ('second_pay_receive', 'Платеж 2 получен'), ('success_fee_wait', 'Финальный платеж ожидание'), ('success_fee_receive', 'Финальный платеж получен'), ('special_terms', 'Особые условия')], default='first_pay', max_length=25, verbose_name='Статус оплаты'),
        ),
    ]
