# Generated by Django 5.0.6 on 2024-06-15 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_user_ride_id_remove_user_traveler_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ride_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='traveler_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
