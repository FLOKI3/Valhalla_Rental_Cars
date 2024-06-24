# Generated by Django 5.0.6 on 2024-06-23 19:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0020_invoicestep1_invoicestep4_alter_reservation_parking_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
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
        migrations.DeleteModel(
            name='InvoiceStep1',
        ),
        migrations.RemoveField(
            model_name='invoicestep2',
            name='client',
        ),
        migrations.RemoveField(
            model_name='invoicestep3',
            name='car',
        ),
        migrations.DeleteModel(
            name='InvoiceStep4',
        ),
        migrations.DeleteModel(
            name='InvoiceStep2',
        ),
        migrations.DeleteModel(
            name='InvoiceStep3',
        ),
    ]