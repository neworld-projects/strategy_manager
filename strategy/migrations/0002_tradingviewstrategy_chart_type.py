# Generated by Django 4.1.4 on 2023-02-25 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradingviewstrategy',
            name='chart_type',
            field=models.IntegerField(choices=[(0, 'sample'), (1, 'heikinashi')], db_index=True, default=0),
        ),
    ]