# Generated by Django 2.0.7 on 2018-07-24 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0011_auto_20180724_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='trip1_time',
            field=models.TimeField(blank=True, default='00:00:00'),
        ),
        migrations.AlterField(
            model_name='groups',
            name='trip2_time',
            field=models.TimeField(blank=True, default='00:00:00'),
        ),
    ]
