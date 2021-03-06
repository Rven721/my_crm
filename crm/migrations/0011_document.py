# Generated by Django 3.0.4 on 2021-12-28 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_event_took_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название документа')),
                ('pages', models.IntegerField(default=1, max_length=3, verbose_name='Число страниц')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='crm.Event', verbose_name='Событие')),
            ],
        ),
    ]
