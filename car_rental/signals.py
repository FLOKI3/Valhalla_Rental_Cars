from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation, Car, Notification, Worker
from django.contrib.auth.models import User, Group

from django.apps import AppConfig

@receiver(post_save, sender=Reservation)
def update_car_status(sender, instance, created, **kwargs):
    if created:
        car = instance.car
        car.status = 'rented'
        car.save()


















@receiver(post_save, sender=Reservation)
def create_reservation_notification(sender, instance, created, **kwargs):
    if created:
        message = f"New reservation added: {instance}"
        recipients = User.objects.all()  # Modify this to filter recipients if needed
        for recipient in recipients:
            Notification.objects.create(message=message, recipient=recipient)
    