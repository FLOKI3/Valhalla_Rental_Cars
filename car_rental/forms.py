from django import forms
from django.forms import ModelForm
from .models import Car, Client, Reservation, Worker, Spend, Invoice, Maintenance
from django.forms import modelformset_factory
from django.contrib.auth.models import User







class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'type',
            'model',
            'model_year',
            'matricule',
            'car_picture',
            'price_day',
            'status',
            'problems',
            'problems_picture',
            'color',
            'car_power',
        ]

        widgets = {
            'type': forms.Select(attrs={'class':'form-control mt-3 mb-3'}),
            'model': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'model_year': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3'}),
            'matricule': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'car_picture': forms.FileInput(attrs={'multiple class':'form-control mt-3 mb-3', 'type':'file'}),
            'price_day': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3'}),
            'status': forms.Select(attrs={'class':'form-control mt-3 mb-3'}),
            'problems': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),

            'problems_picture': forms.FileInput(attrs={'class':'form-control mt-3 mb-3', 'type':'file'}),
            'color': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'car_power': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3'}),
        }



        
















class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'client_picture',
            'first_name',
            'last_name',
            'CIN',
            'birth_date',
            'driver_license_number',
            'gender',
            'phone_number',
            'email',
            'address',
            'passport_number',
            'passport_delivery',
            ]
        
        widgets = {
            'client_picture': forms.ClearableFileInput(attrs={'class':'form-control mt-3 mb-3', 'id':'id_client_picture'}),
            'first_name': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'last_name': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'CIN': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'birth_date': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'date'}),
            'driver_license_number': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3'}),
            'gender': forms.Select(attrs={'class':'form-control mt-3 mb-3', 'type':'checkbox'}),
            'phone_number': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'tel', 'placeholder':'+212'}),
            'email': forms.EmailInput(attrs={'class':'form-control mt-3 mb-3', 'type':'email'}),
            'address': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'passport_number': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'passport_delivery': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'date'}),
        }
        

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'car',
            'client',
            'livraison_location',
            'livraison_time',
            'guarantee',
            'money_guarantee',
            'start_mileage',
            'start_date',
            'end_date',

            'status',
            'car_status',
            'worker',
            'recuperation_time',
            'recuperation_location',
            'end_mileage',
            'report',
            'parking',
            'discount',
        ]

        widgets = {
            'status': forms.Select(attrs={'class':'form-control mt-3 mb-3'}),
            'car_status': forms.Select(attrs={'class':'form-control mt-3 mb-3'}),
            'worker': forms.Select(attrs={'class':'form-control mt-3 mb-3'}),
            'recuperation_time': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'time'}),
            'recuperation_location': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'report': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'parking': forms.Select(attrs={'class':'form-control mt-3 mb-3'}),

            'car': forms.Select(attrs={'class':'form-control mt-3 mb-3'}),
            'client': forms.Select(attrs={'class':'form-control mt-3 mb-3'}),
            'livraison_location': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'livraison_time': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'time'}),
            'guarantee': forms.Select(attrs={'class':'form-control mt-3 mb-3'}),
            'money_guarantee': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3'}),
            'start_mileage': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3'}),
            'end_mileage': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3'}),
            'start_date': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'date'}),
            'end_date': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'date'}),
            'discount': forms.NumberInput(attrs={'class':'form-control', 'type':'number'}),
        }


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = [
            'user',
            'avatar',
            'first_name',
            'last_name',
            'CIN',
            'birth_date',
            'address',
            'driver_license_number',
            'phone_number',
            'gender',
            'email',
        ]
        widgets = {
            'user': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control mt-3 mb-3'}),
            'first_name': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'last_name': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'CIN': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
            'birth_date': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'date'}),
            'driver_license_number': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3'}),
            'gender': forms.Select(attrs={'class':'form-control mt-3 mb-3', 'type':'checkbox'}),
            'phone_number': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'tel', 'placeholder':'+212'}),
            'email': forms.EmailInput(attrs={'class':'form-control mt-3 mb-3', 'type':'email'}),
            'address': forms.Textarea(attrs={'class':'form-control mt-3 mb-3'}),
        }





class SpendForm(forms.ModelForm):
    class Meta:
        model = Spend
        fields = {
            'entry_date',
            'entry_amount',
            'entry_client',
            'entry_worker',
            'entry_description',
            'entry_mode',
            'entry_car',
            
            'expense_date',
            'expense_amount',
            'expense_client',
            'expense_worker',
            'expense_description',
            'expense_mode',
            'expense_car',
        }
        widgets = {
            'entry_date': forms.NumberInput(attrs={'class':'form-control', 'type':'date'}),
            'entry_amount': forms.NumberInput(attrs={'class':'form-control', 'type':'number'}),
            'entry_client': forms.Select(attrs={'class':'form-control'}),
            'entry_worker': forms.Select(attrs={'class':'form-control'}),
            'entry_car': forms.Select(attrs={'class':'form-control'}),
            'entry_description': forms.Textarea(attrs={'class':'form-control'}),
            'entry_mode': forms.Select(attrs={'class':'form-control'}),
            
            'expense_date': forms.NumberInput(attrs={'class':'form-control', 'type':'date'}),
            'expense_amount': forms.NumberInput(attrs={'class':'form-control', 'type':'number'}),
            'expense_client': forms.Select(attrs={'class':'form-control'}),
            'expense_worker': forms.Select(attrs={'class':'form-control'}),
            'expense_car': forms.Select(attrs={'class':'form-control'}),
            'expense_description': forms.Textarea(attrs={'class':'form-control'}),
            'expense_mode': forms.Select(attrs={'class':'form-control'}),
        }










class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'invoice_id',
            'payment_date',
            'client',
            'car',
            'start_date',
            'end_date',
            'discount',
        ]
        widgets = {
            'invoice_id': forms.NumberInput(attrs={'class':'form-control', 'type':'number'}),
            'payment_date': forms.NumberInput(attrs={'class':'form-control', 'type':'date'}),
            'client': forms.Select(attrs={'class':'form-control'}),
            'car': forms.Select(attrs={'class':'form-control'}),
            'start_date': forms.NumberInput(attrs={'class':'form-control', 'type':'date'}),
            'end_date': forms.NumberInput(attrs={'class':'form-control', 'type':'date'}),
            'discount': forms.NumberInput(attrs={'class':'form-control', 'type':'number'}),
        }





class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            'car',
            'insurance_start',
            'insurance_end',
            'technical_visit',
            'oil_change',
        ]
        widgets = {
            'car': forms.Select(attrs={'class':'form-control mt-3 mb-3'}),
            'insurance_start': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'date'}),
            'insurance_end': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'date'}),
            'technical_visit': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'date'}),
            'oil_change': forms.NumberInput(attrs={'class':'form-control mt-3 mb-3', 'type':'number', 'placeholder':'Mileage'}),
        }





















        