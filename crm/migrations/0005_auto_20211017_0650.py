# Generated by Django 3.0.4 on 2021-10-17 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20211017_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_deliver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='crm.ProjectDeliver', verbose_name='Источник проекта'),
        ),
    ]