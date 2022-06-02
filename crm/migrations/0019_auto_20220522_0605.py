# Generated by Django 3.0.4 on 2022-05-22 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0018_auto_20220522_0433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание задачи'),
        ),
        migrations.RemoveField(
            model_name='task',
            name='doers',
        ),
        migrations.AddField(
            model_name='task',
            name='doers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Исполнители'),
        ),
        migrations.RemoveField(
            model_name='task',
            name='events',
        ),
        migrations.AddField(
            model_name='task',
            name='events',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='crm.Event', verbose_name='События'),
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NEW', 'Новая задача'), ('PROGRESS', 'В работе'), ('DONE', 'Завершено')], max_length=10, verbose_name='Статус')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='crm.Task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Статус задачи',
                'verbose_name_plural': 'Статусы задачи',
            },
        ),
    ]