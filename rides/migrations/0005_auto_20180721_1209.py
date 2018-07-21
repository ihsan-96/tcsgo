# Generated by Django 2.0.7 on 2018-07-21 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0004_groupshistory_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='end_point',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='end_point', to='rides.Points'),
        ),
        migrations.AlterField(
            model_name='groups',
            name='start_point',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='start_point', to='rides.Points'),
        ),
    ]