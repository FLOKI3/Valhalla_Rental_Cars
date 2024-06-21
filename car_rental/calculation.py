
from decimal import Decimal
from .models import Reservation, Spend  # Adjust the import path based on your project structure

def calculate_total_amount():
    reservations = Reservation.objects.all()
    total_amount = Decimal('0.00')

    for reservation in reservations:
        total_amount += reservation.total_amount()

    return total_amount

def calculate_final_amount(spends):
    final_amount = calculate_total_amount()

    for spend in spends:
        if spend.entry_amount:
            final_amount += spend.entry_amount
        if spend.expense_amount:
            final_amount -= spend.expense_amount
    return final_amount