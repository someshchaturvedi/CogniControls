# Generated by Django 2.0.3 on 2018-03-21 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controls', '0003_auto_20180321_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='controls1_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='controls2_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]