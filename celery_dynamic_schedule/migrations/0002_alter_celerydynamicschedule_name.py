# Generated by Django 4.1.4 on 2023-01-04 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celery_dynamic_schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celerydynamicschedule',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
