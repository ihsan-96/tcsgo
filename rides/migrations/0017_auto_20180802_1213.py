# Generated by Django 2.0.7 on 2018-08-02 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0016_auto_20180728_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.Cars'),
        ),
    ]
