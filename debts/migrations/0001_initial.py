# Generated by Django 3.0.4 on 2022-08-30 06:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Имя')),
                ('comment', models.CharField(blank=True, max_length=300, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Основание',
                'verbose_name_plural': 'Основания',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Персона',
                'verbose_name_plural': 'Персоны',
            },
        ),
        migrations.CreateModel(
            name='Transh',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Дата')),
                ('charge', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('return_required', models.BooleanField(default=True)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transhes', to='debts.Expense', verbose_name='Основание')),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='debts.Person', verbose_name='Плательщик')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receeves', to='debts.Person', verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Транш',
                'verbose_name_plural': 'Транши',
            },
        ),
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('creditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credits', to='debts.Person', verbose_name='Кредитор')),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debts', to='debts.Person', verbose_name='Должник')),
            ],
            options={
                'verbose_name': 'Долг',
                'verbose_name_plural': 'Долги',
            },
        ),
    ]
