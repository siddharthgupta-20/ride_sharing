# Generated by Django 5.0.6 on 2024-06-14 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_id', models.CharField(max_length=100, unique=True)),
                ('driver_name', models.CharField(max_length=100)),
                ('driver_phone_number', models.CharField(max_length=15)),
                ('cab_number', models.CharField(max_length=15)),
                ('start_location', models.CharField(max_length=255)),
                ('end_location', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]