# Generated by Django 2.0.7 on 2018-07-17 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_number', models.CharField(max_length=25, unique=True)),
                ('car_name', models.CharField(max_length=25)),
                ('mileage', models.IntegerField(default=30)),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats_offered', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], default=3)),
                ('pay_status', models.IntegerField(choices=[(0, 'no pay'), (1, 'pay')], default=0)),
                ('trip1_time', models.TimeField()),
                ('trip2_time', models.TimeField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.Cars')),
            ],
        ),
        migrations.CreateModel(
            name='GroupsHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_status', models.CharField(max_length=10)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.Cars')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_type', models.CharField(choices=[('1', 'trip1'), ('2', 'trip2'), ('3', 'both')], max_length=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.Groups')),
            ],
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_status', models.CharField(choices=[('1', 'pending'), ('2', 'rejected'), ('3', 'accepted')], default='pending', max_length=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.Groups')),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_point', to='rides.Points')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('middle_name', models.CharField(blank=True, max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('sex', models.CharField(choices=[('1', 'male'), ('2', 'female'), ('3', 'other')], max_length=10)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('dl_number', models.CharField(max_length=15, unique=True)),
                ('blood_group', models.CharField(choices=[('1', 'A+ve'), ('2', 'A-ve'), ('3', 'B+ve'), ('4', 'B-ve'), ('5', 'O+ve'), ('6', 'O-ve'), ('7', 'AB+ve'), ('8', 'AB-ve')], max_length=5)),
                ('employee_number', models.CharField(max_length=25, unique=True)),
                ('card_number', models.CharField(max_length=25, unique=True)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='requests',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.Users'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.Users'),
        ),
        migrations.AddField(
            model_name='groupshistory',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='rides.Points'),
        ),
        migrations.AddField(
            model_name='groupshistory',
            name='members',
            field=models.ManyToManyField(to='rides.Users'),
        ),
        migrations.AddField(
            model_name='groupshistory',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_history', to='rides.Users'),
        ),
        migrations.AddField(
            model_name='groupshistory',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='rides.Points'),
        ),
        migrations.AddField(
            model_name='groups',
            name='end_point',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='end_point', to='rides.Points'),
        ),
        migrations.AddField(
            model_name='groups',
            name='members',
            field=models.ManyToManyField(through='rides.Membership', to='rides.Users'),
        ),
        migrations.AddField(
            model_name='groups',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='rides.Users'),
        ),
        migrations.AddField(
            model_name='groups',
            name='start_point',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='start_point', to='rides.Points'),
        ),
        migrations.AddField(
            model_name='groups',
            name='trip1_intermediate_points',
            field=models.ManyToManyField(related_name='trip1_intermediate_points', to='rides.Points'),
        ),
        migrations.AddField(
            model_name='groups',
            name='trip2_intermediate_points',
            field=models.ManyToManyField(related_name='trip2_intermediate_points', to='rides.Points'),
        ),
        migrations.AddField(
            model_name='cars',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.Users'),
        ),
        migrations.AlterUniqueTogether(
            name='requests',
            unique_together={('group', 'user', 'point')},
        ),
        migrations.AlterUniqueTogether(
            name='groups',
            unique_together={('owner', 'car')},
        ),
    ]
