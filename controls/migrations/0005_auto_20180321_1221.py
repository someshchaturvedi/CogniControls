# Generated by Django 2.0.3 on 2018-03-21 12:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controls', '0004_auto_20180321_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='controls1_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkin',
            name='controls2_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='controls1_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='controls2_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]