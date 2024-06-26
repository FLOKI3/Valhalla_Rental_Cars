# Generated by Django 5.0.6 on 2024-06-26 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0005_alter_reservation_parking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='parking',
            field=models.CharField(blank=True, choices=[('parking_b', 'Parking B'), ('parking_a', 'Parking A')], max_length=50, null=True),
        ),
    ]
