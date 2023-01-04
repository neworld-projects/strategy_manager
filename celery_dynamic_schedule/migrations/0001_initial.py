# Generated by Django 4.1.4 on 2023-01-04 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryDynamicSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('task', models.CharField(max_length=150)),
                ('task_kwargs', models.JSONField(default={})),
                ('last_run', models.DateTimeField(blank=True, null=True)),
                ('crontab_code', models.CharField(max_length=150)),
                ('run_crontab_minute', models.JSONField(default={})),
                ('run_crontab_hour', models.JSONField(default={})),
                ('run_crontab_day_of_week', models.JSONField(default={})),
                ('run_crontab_day_of_month', models.JSONField(default={})),
                ('run_crontab_month_of_year', models.JSONField(default={})),
            ],
        ),
    ]
