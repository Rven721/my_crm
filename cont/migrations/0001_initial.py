# Generated by Django 3.0.4 on 2022-10-07 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crm', '0040_auto_20221005_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('data', models.TextField(verbose_name='Свдения о контрагенте')),
            ],
            options={
                'verbose_name': 'Агент',
                'verbose_name_plural': 'Агенты',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20, verbose_name='')),
                ('date', models.DateField(verbose_name='Дата')),
                ('payment_stauts', models.CharField(choices=[('first_pay_wait', 'Платеж 1 ожидание'), ('second_pay_receive', 'Платеж 1 пулучен'), ('second_pay_wait', 'Платеж 2 ожидание'), ('second_pay_receive', 'Платеж 2 получен'), ('success_fee_wait', 'Финальный платеж ожидание'), ('success_fee_receive', 'Финальный платеж получен')], default='first_pay', max_length=25, verbose_name='Статус оплаты')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cont.Agent', verbose_name='Агент')),
                ('projct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Project', verbose_name='Проект')),
            ],
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('first_pay', models.FloatField(verbose_name='Первый платеж')),
                ('second_pay', models.FloatField(verbose_name='Второй платеж')),
                ('success_fee', models.FloatField(verbose_name='Плата за успех')),
                ('success_fee_base', models.CharField(choices=[('grant', 'Грант'), ('project', 'Проект')], max_length=10, verbose_name='База для расчета')),
                ('team_fee', models.FloatField(verbose_name='Выручка команды')),
            ],
            options={
                'verbose_name': 'Условия',
                'verbose_name_plural': 'Условия',
            },
        ),
        migrations.CreateModel(
            name='StatusChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='дата')),
                ('status', models.CharField(max_length=50, verbose_name='status')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cont.Contract', verbose_name='Проект')),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='terms',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cont.Terms', verbose_name='Условия'),
        ),
    ]
