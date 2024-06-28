from django.utils.timezone import now, timedelta
from .models import Notification, Maintenance, Reservation

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        unread_notifications = notifications.filter(is_read=False)

        # Maintenance Notification Logic
        warning_date = now().date() + timedelta(days=2)
        maintenances = Maintenance.objects.all()

        for maintenance in maintenances:
            latest_reservation = Reservation.objects.filter(car=maintenance.car).order_by('-end_date').first()
            if latest_reservation:
                end_mileage = latest_reservation.end_mileage if latest_reservation.end_mileage is not None else 0
            else:
                end_mileage = 0  # or some default value if there's no reservation

            # Check for insurance end notification
            if maintenance.insurance_end and maintenance.insurance_end <= warning_date:
                message = f"Insurance for {maintenance.car} is about to expire."
                event_identifier = f"{maintenance.car.id}_insurance_expiring"
                Notification.create_notification(message, request.user, event_identifier)

            # Check for technical visit end notification
            if maintenance.technical_visit and maintenance.technical_visit <= warning_date:
                message = f"Technical visit for {maintenance.car} is about to expire."
                event_identifier = f"{maintenance.car.id}_technical_visit_expiring"
                Notification.create_notification(message, request.user, event_identifier)

            # Check for oil change notification
            if maintenance.oil_change and maintenance.oil_change <= end_mileage:
                message = f"Oil change needed for {maintenance.car}."
                event_identifier = f"{maintenance.car.id}_oil_change_needed"
                Notification.create_notification(message, request.user, event_identifier)

        # End Reservation Notification Logic
        upcoming_end_date = now().date() + timedelta(days=1)
        reservations = Reservation.objects.filter(end_date=upcoming_end_date)

        for reservation in reservations:
            message = f"Reservation for {reservation.car} is ending soon."
            event_identifier = f"{reservation.id}_reservation_ending"
            Notification.create_notification(message, request.user, event_identifier)

        return {
            'notifications': notifications,
            'unread_notifications': unread_notifications,
        }
    return {
        'notifications': [],
        'unread_notifications': [],
    }
