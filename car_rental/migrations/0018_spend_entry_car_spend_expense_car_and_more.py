# Generated by Django 5.0.6 on 2024-06-21 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0017_alter_reservation_parking'),
    ]

    operations = [
        migrations.AddField(
            model_name='spend',
            name='entry_car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entry_spends', to='car_rental.car'),
        ),
        migrations.AddField(
            model_name='spend',
            name='expense_car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expense_spends', to='car_rental.car'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='parking',
            field=models.CharField(blank=True, choices=[('parking_a', 'Parking A'), ('parking_b', 'Parking B')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('ended', 'Ended')], default='active', max_length=10, null=True),
        ),
    ]