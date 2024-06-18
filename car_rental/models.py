from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime, date
from decimal import Decimal
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    type = models.CharField(max_length=50)
    type_picture = models.ImageField(upload_to='tyoe-pictures/', null=True, blank=True)

    def __str__(self):
        return self.type
        


class Car(models.Model):

    car_status = [
        ('available','Available'),
        ('broke','Broke'),
        ('unavailable','Unavailable'),
        ('rented','Rented'),

    ]

    type = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    model = models.CharField(max_length=50)
    model_year = models.IntegerField(null=True, blank=True)
    matricule = models.CharField(max_length=50, null=False, blank=False)
    car_picture = models.ImageField(upload_to='car-pictures/', null=True, blank=True)
    price_day = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    availability = models.BooleanField(default=True)
    status = models.CharField(max_length=50, choices=car_status, default='available', null=True, blank=True)
    problems = models.CharField(max_length=500, null=True, blank=True)
    problems_picture = models.ImageField(upload_to='car-pictures/', null=True, blank=True)
    color = models.CharField(max_length=10, null=True, blank=True)
    car_power = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.model
    




    

class Client(models.Model):

    genders = [
        ('male','Male'),
        ('female','Female'),
    ]

    client_picture = models.ImageField(upload_to='client-profile/', null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    CIN = models.CharField(max_length=50)
    birth_date = models.DateField()
    driver_license_number = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=genders)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=50, null=True, blank=True)
    passport_delivery = models.DateField(null=True, blank=True)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    


    def total_amount_spent(self):
        # Calculate total amount spent on reservations
        total = sum(reservation.calculate_total_cost() for reservation in self.reservation_set.all())
        return total










########################


class Worker(models.Model):

    genders = [
        ('male','Male'),
        ('female','Female'),
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='worker-profile/', null=True, blank=True)

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    CIN = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    driver_license_number = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=genders, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
    def __str__(self):
        return self.user.username


########################


class Reservation(models.Model):
    reservation_status = {
        ('active','Active'),
        ('ended','Ended'),
    }
    parking_locations = {
        ('parking_a','Parking A'),
        ('parking_b','Parking B'),
    }

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    livraison_location = models.CharField(max_length=50)
    livraison_time = models.TimeField(auto_now=False, auto_now_add=False)
    money_guarantee = models.IntegerField(null=True, blank=True)
    fuel_gas = models.IntegerField(null=True, blank=True)
    parking = models.CharField(max_length=50, choices=parking_locations, null=True, blank=True)
    availability = models.BooleanField(default=True)

    status = models.CharField(max_length=10, choices=reservation_status, default='active', null=True, blank=True)
    car_status = models.CharField(max_length=50, choices=Car.car_status, null=True, blank=True, default='rented')
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT, null=True, blank=True)
    recuperation_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    recuperation_location = models.CharField(max_length=50, null=True, blank=True)
    report = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def total_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return 0

    def total_amount(self):
        return self.total_days() * self.car.price_day if self.start_date and self.end_date else Decimal('0.00')


    def calculate_total_cost(self):
        # Calculate the number of days rented, ensuring start and end date count correctly
        duration = (self.end_date - self.start_date).days
        if duration == 0:  # Same day rental
            duration = 1
        total_cost = duration * self.car.price_day
        return total_cost
    

    def __str__(self):
        return self.car.model
    








    

















class Notification(models.Model):
    message = models.CharField(max_length=255)
    recipient = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

















class UserActionLog(models.Model):
    ACTION_CHOICES = [
        ('add', 'Add'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('create', 'Create'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"