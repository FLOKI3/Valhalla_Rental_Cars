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
        return f'{self.model} ({self.matricule})'
    
    def total_amount_spent(self):
        # Calculate total amount spent on reservations
        total_reservations = sum(reservation.calculate_total_cost() for reservation in self.reservation_set.all())

        # Calculate total entry amount (income)
        total_entry_amount = sum(spend.entry_amount for spend in self.entry_spends.all() if spend.entry_amount is not None)

        # Calculate total expense amount
        total_expense_amount = sum(spend.expense_amount for spend in self.expense_spends.all() if spend.expense_amount is not None)

        # Total amount spent is total reservations + total entry amount - total expense amount
        total_spent = total_reservations + total_entry_amount - total_expense_amount
        return total_spent




    

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
        total_reservations = sum(reservation.calculate_total_cost() for reservation in self.reservation_set.all())

        # Calculate total entry amount (income)
        total_entry_amount = sum(spend.entry_amount for spend in self.entry_spends.all() if spend.entry_amount is not None)

        # Calculate total expense amount
        total_expense_amount = sum(spend.expense_amount for spend in self.expense_spends.all() if spend.expense_amount is not None)

        # Total amount spent is total reservations + total entry amount - total expense amount
        total_spent = total_reservations + total_entry_amount - total_expense_amount
        return total_spent









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
    guarantee_choices = {
        ('money','Money'),
        ('passport','Passport'),
    }

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    livraison_location = models.CharField(max_length=50)
    livraison_time = models.TimeField(auto_now=False, auto_now_add=False)
    guarantee = models.CharField(max_length=50, choices=guarantee_choices, null=True, blank=True)
    money_guarantee = models.IntegerField(null=True, blank=True)
    start_mileage = models.IntegerField(null=True, blank=True)
    parking = models.CharField(max_length=50, choices=parking_locations, null=True, blank=True)
    availability = models.BooleanField(default=True)

    status = models.CharField(max_length=10, choices=reservation_status, default='active', null=True, blank=True)
    car_status = models.CharField(max_length=50, choices=Car.car_status, null=True, blank=True, default='rented')
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT, null=True, blank=True)
    recuperation_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    recuperation_location = models.CharField(max_length=50, null=True, blank=True)
    end_mileage = models.IntegerField(null=True, blank=True)
    report = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)


    def total_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return 0

    def total_amount(self):
        if self.start_date and self.end_date:
            base_amount = self.total_days() * self.car.price_day
            discount_amount = self.discount or 0
            return base_amount - discount_amount
        return Decimal('0.00')

    def calculate_total_cost(self):
        # Calculate the number of days rented, ensuring start and end date count correctly
        duration = (self.end_date - self.start_date).days
        if duration == 0:  # Same day rental
            duration = 1
        base_cost = duration * self.car.price_day
        discount_amount = self.discount or 0
        total_cost = base_cost - discount_amount
        return total_cost
    

    def save(self, *args, **kwargs):
        if not self.pk:  # if this is a new reservation
            latest_reservation = Reservation.objects.filter(car=self.car).order_by('-end_date').first()
            if latest_reservation:
                latest_reservation.parking = None
                latest_reservation.save()
        super(Reservation, self).save(*args, **kwargs)
   

    def __str__(self):
        return self.car.model
    








    

















class Notification(models.Model):
    message = models.CharField(max_length=255)
    recipient = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    event_identifier = models.CharField(max_length=50, default='default_identifier')

    def __str__(self):
        return self.message

    @classmethod
    def create_notification(cls, message, recipient, event_identifier):
        notification, created = cls.objects.get_or_create(
            recipient=recipient,
            event_identifier=event_identifier,
            defaults={'message': message}
        )
        if not created:
            notification.message = message
            notification.save()
            
















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
    


class Spend(models.Model):
    payment_mode = [
        ('cash','Cash'),
        ('bank_check','Bank Check'),
    ]

    entry_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    entry_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    entry_client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True, related_name='entry_spends')
    entry_worker = models.ForeignKey(Worker, on_delete=models.PROTECT, null=True, blank=True, related_name='entry_spends')
    entry_car = models.ForeignKey(Car, on_delete=models.PROTECT, null=True, blank=True, related_name='entry_spends')
    entry_description = models.CharField(max_length=5000, null=True, blank=True)
    entry_mode = models.CharField(choices=payment_mode, max_length=50, null=True, blank=True)
    
    expense_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expense_client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True, related_name='expense_spends')
    expense_worker = models.ForeignKey(Worker, on_delete=models.PROTECT, null=True, blank=True, related_name='expense_spends')
    expense_description = models.CharField(max_length=5000, null=True, blank=True)
    expense_mode = models.CharField(choices=payment_mode, max_length=50, null=True, blank=True)
    expense_car = models.ForeignKey(Car, on_delete=models.PROTECT, null=True, blank=True, related_name='expense_spends')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    

class Invoice(models.Model):
    invoice_id = models.CharField(max_length=500)
    payment_date = models.DateField(auto_now=False, auto_now_add=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
        
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)


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
        return self.invoice_id
    





class Maintenance(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    insurance_start = models.DateField(auto_now=False, auto_now_add=False)
    insurance_end = models.DateField(auto_now=False, auto_now_add=False)
    technical_visit = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    oil_change = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    

    def get_status(self):
        today = date.today()
        if self.insurance_end < today or (self.technical_visit and self.technical_visit < today):
            return 'danger'
        return 'success'
    
    

    def __str__(self):
        return f'{self.car}'
