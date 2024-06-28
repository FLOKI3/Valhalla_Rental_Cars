# Generated by Django 5.0.6 on 2024-06-27 23:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0007_reservation_guarantee_alter_reservation_parking'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='guarantee',
            field=models.CharField(blank=True, choices=[('passport', 'Passport'), ('money', 'Money')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='parking',
            field=models.CharField(blank=True, choices=[('parking_b', 'Parking B'), ('parking_a', 'Parking A')], max_length=50, null=True),
        ),
    ]