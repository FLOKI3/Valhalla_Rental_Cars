
from decimal import Decimal
from .models import Reservation  # Adjust the import path based on your project structure

def calculate_total_amount():
    reservations = Reservation.objects.all()
    total_amount = Decimal('0.00')

    for reservation in reservations:
        total_amount += reservation.total_amount()

    return total_amount