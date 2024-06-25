# Generated by Django 5.0.6 on 2024-06-25 15:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('type_picture', models.ImageField(blank=True, null=True, upload_to='tyoe-pictures/')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_picture', models.ImageField(blank=True, null=True, upload_to='client-profile/')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('CIN', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('driver_license_number', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(max_length=50)),
                ('passport_number', models.CharField(blank=True, max_length=50, null=True)),
                ('passport_delivery', models.DateField(blank=True, null=True)),
                ('availability', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('model_year', models.IntegerField(blank=True, null=True)),
                ('matricule', models.CharField(max_length=50)),
                ('car_picture', models.ImageField(blank=True, null=True, upload_to='car-pictures/')),
                ('price_day', models.DecimalField(decimal_places=2, max_digits=10)),
                ('availability', models.BooleanField(default=True)),
                ('status', models.CharField(blank=True, choices=[('available', 'Available'), ('broke', 'Broke'), ('unavailable', 'Unavailable'), ('rented', 'Rented')], default='available', max_length=50, null=True)),
                ('problems', models.CharField(blank=True, max_length=500, null=True)),
                ('problems_picture', models.ImageField(blank=True, null=True, upload_to='car-pictures/')),
                ('color', models.CharField(blank=True, max_length=10, null=True)),
                ('car_power', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='car_rental.category')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(max_length=500)),
                ('payment_date', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_rental.car')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_rental.client')),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance_start', models.DateField()),
                ('insurance_end', models.DateField()),
                ('technical_visit', models.DateField(blank=True, null=True)),
                ('oil_change', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='car_rental.car')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('add', 'Add'), ('update', 'Update'), ('delete', 'Delete'), ('create', 'Create')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='worker-profile/')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('CIN', models.CharField(blank=True, max_length=50, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('driver_license_number', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('availability', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Spend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField(blank=True, null=True)),
                ('entry_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('entry_description', models.CharField(blank=True, max_length=5000, null=True)),
                ('entry_mode', models.CharField(blank=True, choices=[('cash', 'Cash'), ('bank_check', 'Bank Check')], max_length=50, null=True)),
                ('expense_date', models.DateField(blank=True, null=True)),
                ('expense_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('expense_description', models.CharField(blank=True, max_length=5000, null=True)),
                ('expense_mode', models.CharField(blank=True, choices=[('cash', 'Cash'), ('bank_check', 'Bank Check')], max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('entry_car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entry_spends', to='car_rental.car')),
                ('entry_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entry_spends', to='car_rental.client')),
                ('expense_car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expense_spends', to='car_rental.car')),
                ('expense_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expense_spends', to='car_rental.client')),
                ('entry_worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entry_spends', to='car_rental.worker')),
                ('expense_worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expense_spends', to='car_rental.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('livraison_location', models.CharField(max_length=50)),
                ('livraison_time', models.TimeField()),
                ('money_guarantee', models.IntegerField(blank=True, null=True)),
                ('start_mileage', models.IntegerField(blank=True, null=True)),
                ('parking', models.CharField(blank=True, choices=[('parking_b', 'Parking B'), ('parking_a', 'Parking A')], max_length=50, null=True)),
                ('availability', models.BooleanField(default=True)),
                ('status', models.CharField(blank=True, choices=[('ended', 'Ended'), ('active', 'Active')], default='active', max_length=10, null=True)),
                ('car_status', models.CharField(blank=True, choices=[('available', 'Available'), ('broke', 'Broke'), ('unavailable', 'Unavailable'), ('rented', 'Rented')], default='rented', max_length=50, null=True)),
                ('recuperation_time', models.TimeField(blank=True, null=True)),
                ('recuperation_location', models.CharField(blank=True, max_length=50, null=True)),
                ('end_mileage', models.IntegerField(blank=True, null=True)),
                ('report', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_rental.car')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_rental.client')),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='car_rental.worker')),
            ],
        ),
    ]
