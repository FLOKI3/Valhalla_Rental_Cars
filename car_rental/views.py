from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CarForm, ClientForm, ReservationForm, WorkerForm, SpendForm, InvoiceForm, MaintenanceForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.db.models import Sum, Q
from datetime import datetime, date, timedelta
from collections import defaultdict
from django.utils.timezone import now

from django.utils.http import urlencode
from car_rental.calculation import calculate_total_amount, calculate_final_amount





# Create your views here.




@login_required
def users_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    context = {
        'users': Worker.objects.all().order_by('-created_at'),
        'profile': Worker.objects.get(user=request.user),
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/workers.html', context)




###################### Login ######################
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('/dashboard')
                else:
                    return redirect('/car-cards')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login')

###################### Dashboard ######################


###################### Cars ######################

@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def cars(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    if request.method == 'POST':
        add_car = CarForm(request.POST, request.FILES)
        if add_car.is_valid():
            car = add_car.save()
            # Log the add action
            UserActionLog.objects.create(
                user=request.user,
                action='add',
                description=f"Added car: {car.model} with Registration N°: {car.matricule}"
            )
        
            return HttpResponseRedirect(reverse('cars'))
        
    cars = Car.objects.all().order_by('-created_at')
    
    for car in cars:
        car.total_spent = car.total_amount_spent()
        max_budget = 50000  # Example maximum budget, adjust according to your needs
        if max_budget > 0:
            car.progress_percentage = (car.total_spent / max_budget) * 100
        else:
            car.progress_percentage = 0

    context = {
        'category': Category.objects.all(),
        'cars': cars,
        'form': CarForm(),
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/cars.html', context)
@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def car_edit(request, id):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    car_id = Car.objects.get(id=id)
    entry_spends = Spend.objects.filter(entry_car=car_id).order_by('-created_at')
    expense_spends = Spend.objects.filter(expense_car=car_id).order_by('-created_at')
    recent_spends = list(entry_spends) + list(expense_spends)
    recent_spends.sort(key=lambda spend: spend.created_at, reverse=True)
    if request.method == 'POST':
        car_save = CarForm(request.POST, request.FILES, instance=car_id)
        if car_save.is_valid():
            car =car_save.save()
            # Log the edit action
            UserActionLog.objects.create(
                user=request.user,
                action='update',
                description=f"Updated car: {car}"
            )
            return HttpResponseRedirect(reverse('cars'))
        

    else:
        car_save = CarForm(instance=car_id)

    context = {
        'form': car_save,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
        'recent_spends': recent_spends,
    }
    return render(request, 'pages/car-edit.html', context)
@login_required
def car_cards(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)

    cars = Car.objects.all().order_by('-created_at')

    warning_date = now().date() + timedelta(days=2)

    for car in cars:
        latest_reservation = Reservation.objects.filter(car=car).order_by('-end_date').first()
        if latest_reservation:
            end_mileage = latest_reservation.end_mileage if latest_reservation.end_mileage is not None else 0
        else:
            end_mileage = 0  # or some default value if there's no reservation

        # Check maintenance status
        maintenance_status = ''

        try:
            maintenance = Maintenance.objects.filter(car=car).latest('created_at')
        except Maintenance.DoesNotExist:
            maintenance = None

        if maintenance:
            if maintenance.insurance_end and maintenance.insurance_end <= warning_date:
                maintenance_status = 'Insurance Expired'
            elif maintenance.technical_visit and maintenance.technical_visit <= warning_date:
                maintenance_status = 'Technical Visit Expired'
            elif maintenance.oil_change and maintenance.oil_change <= end_mileage:
                maintenance_status = 'Oil Change Needed'

        car.maintenance_status = maintenance_status

    context = {
        'cars': cars,
        'form': CarForm(),
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/cars-card.html', context)
@login_required
def car_detail(request, id):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    car = get_object_or_404(Car, id=id)
    latest_reservation = Reservation.objects.filter(car=car).order_by('-end_date').first()
    parking = latest_reservation.parking
    
    if latest_reservation:
        end_mileage = latest_reservation.end_mileage if latest_reservation.end_mileage is not None else latest_reservation.start_mileage
        end_mileage = end_mileage if end_mileage is not None else 0
    else:
        end_mileage = 0
    
    # Fetch the latest maintenance record for the car
    maintenance = Maintenance.objects.filter(car=car).order_by('-created_at').first()

    warning_date = now().date() + timedelta(days=2)

    maintenance_status = None
    if maintenance:
        if maintenance.insurance_end and maintenance.insurance_end <= warning_date:
            maintenance_status = "Insurance Expired"
        elif maintenance.technical_visit and maintenance.technical_visit <= warning_date:
            maintenance_status = "Technical Visit Expired"
        elif maintenance.oil_change and end_mileage >= maintenance.oil_change:
            maintenance_status = "Oil Change Needed"
        else:
            maintenance_status = "All Good"
    # Fetch the latest maintenance record for the car


    context = {
        'latest_reservation': latest_reservation,
        'car': car,
        'notifications': notifications,
        'unread_notifications': unread_notifications,        
        'end_mileage': end_mileage,        
        'maintenance_status': maintenance_status,        
        'parking': parking,        
    }
    return render(request, 'pages/car-detail.html', context)
@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def car_delete(request, id):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    car_delete = get_object_or_404(Car, id=id)
    if request.method == 'POST':


        car = get_object_or_404(Car, id=id)

        if car.status == 'rented':
            messages.error(request, "Cannot delete the car because it is currently rented.")
            return redirect('cars')


        car_delete.delete()
        messages.success(request, "Car deleted successfully.")
        # Log the add action
        UserActionLog.objects.create(
            user=request.user,
            action='delete',
            description=f"Deleted car: {car.model} with Registration N°: {car.matricule}"
        )
        return redirect('/cars')
    
    
    context = {
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    
    return render(request, 'pages/car-delete.html', context)

###################### Clients ######################

@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def clients(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    if request.method == 'POST':
        add_client = ClientForm(request.POST, request.FILES)
        if add_client.is_valid():
            add_client.save()

            # Log the action
            UserActionLog.objects.create(
                user=request.user,
                action='create',
                description=f"Created client '{add_client.cleaned_data['first_name']} {add_client.cleaned_data['last_name']}'"
            )

            return HttpResponseRedirect('/clients')
        

    clients = Client.objects.all().order_by('-created_at')
    for client in clients:
        client.total_spent = client.total_amount_spent()

    context = {
        'clients': clients,
        'form': ClientForm(),
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/clients.html', context)
@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def client_edit(request, id):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    client_id = Client.objects.get(id=id)
    entry_spends = Spend.objects.filter(entry_client=client_id).order_by('-created_at')
    expense_spends = Spend.objects.filter(expense_client=client_id).order_by('-created_at')
    recent_spends = list(entry_spends) + list(expense_spends)
    recent_spends.sort(key=lambda spend: spend.created_at, reverse=True)
    if request.method == 'POST':
        client_save = ClientForm(request.POST, request.FILES, instance=client_id)
        if client_save.is_valid():
            client_save.save()

            # Log the action
            UserActionLog.objects.create(
                user=request.user,
                action='update',
                description=f"Updated client '{client_id.first_name} {client_id.last_name}'"
            )

            return HttpResponseRedirect(reverse('clients'))
    else:
        client_save = ClientForm(instance=client_id)
    
    

    context = {
        'form': client_save,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
        'recent_spends': recent_spends,
    }
    return render(request, 'pages/client-edit.html', context)
@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def client_profile_delete(request, client_id):
    client_profile = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client_profile.client_picture.delete()  
        client_profile.client_picture = None  
        client_profile.save()
        return redirect('clients', profile_id=client_id)   

@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def client_delete(request, id):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    client_delete = get_object_or_404(Client, id=id)
    
    # Check if the client has any active reservations with a rented car
    active_reservations = Reservation.objects.filter(client=client_delete, car__status='rented').exists()

    if request.method == 'POST':
        if active_reservations:
            messages.error(request, "This client cannot be deleted because they have a rented car.")
        else:
            try:
                # Log the action
                UserActionLog.objects.create(
                    user=request.user,
                    action='delete',
                    description=f"Deleted client '{client_delete.first_name} {client_delete.last_name}'"
                )
                client_delete.delete()
                messages.success(request, "Client successfully deleted.")
            except:
                messages.error(request, "An error occurred while trying to delete the client.")
        
        return redirect('/clients')
    
    

    context = {
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }

    return render(request, 'pages/client-delete.html', context)

###################### Reservations ######################

@login_required
def reservations(request):
    if request.method == 'POST':
        add_reservation = ReservationForm(request.POST, request.FILES)
        if add_reservation.is_valid():
            reservation = add_reservation.save()

            # Log the action
            UserActionLog.objects.create(
                user=request.user,
                action='add',
                description=f"Added reservation for {reservation.client.first_name} {reservation.client.last_name}"
            )
            
            return redirect('reservations')
    
    # Default queryset to display all reservations sorted by created_at
    reservations_queryset = Reservation.objects.all().order_by('-created_at')

    # Filtering reservations based on status parameter
    status = request.GET.get('status')
    if status == 'active':
        reservations_queryset = reservations_queryset.filter(status='active')
    elif status == 'ended':
        reservations_queryset = reservations_queryset.filter(status='ended')

    # Fetch notifications and mark them as read when viewed
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)

    if request.method == 'GET' and 'notification_id' in request.GET:
        notification_id = request.GET.get('notification_id')
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
            notification.is_read = True
            notification.save()
        except Notification.DoesNotExist:
            pass  # Handle case where notification is not found

   

    context = {
        'reservations': reservations_queryset,
        'cars': Car.objects.all(),
        'category': Category.objects.all(),
        'clients': Client.objects.all(),
        'form': ReservationForm(),
        'workers': Worker.objects.all(),
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/reservations.html', context)
@login_required
def reservation_edit(request, id):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    reservation_id = Reservation.objects.get(id=id)
    if request.method == 'POST':
        reservation_save = ReservationForm(request.POST, request.FILES, instance=reservation_id)
        if reservation_save.is_valid():
            reservation = reservation_save.save(commit=False)
            reservation.car.status = reservation.car_status
            reservation.car.save()
            reservation.save()

            # Log the action
            UserActionLog.objects.create(
                user=request.user,
                action='update',
                description=f"update reservation for {reservation.client.first_name} {reservation.client.last_name}"
            )

            return HttpResponseRedirect(reverse('reservations'))
    else:
        reservation_save = ReservationForm(instance=reservation_id)
    context = {
        'reservation': reservation_id,
        'reservations': Reservation.objects.all(),
        'form': reservation_save,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/reservation-edit.html', context)
@login_required
def reservation_delete(request, id):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    reservation_delete = get_object_or_404(Reservation, id=id)
    if request.method == 'POST':
        reservation_delete.delete()

        # Log the action
        UserActionLog.objects.create(
            user=request.user,
            action='delete',
            description=f"Deleted reservation for {reservation_delete.client.first_name} {reservation_delete.client.last_name}"
        )

        return redirect('/reservations')
    
    

    context = {
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    
    return render(request, 'pages/reservation-delete.html', context)

###################### Stats ######################
######################
######################
def calculate_weekly_totals():
    reservations = Reservation.objects.all()
    weekly_totals = defaultdict(Decimal)

    for reservation in reservations:
        start_date = reservation.start_date
        end_date = reservation.end_date
        if start_date and end_date:
            week_start = start_date - timedelta(days=start_date.weekday())
            week_end = end_date - timedelta(days=end_date.weekday())
            for single_date in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
                week = single_date - timedelta(days=single_date.weekday())
                weekly_totals[week] += reservation.total_amount()

    sorted_weekly_totals = sorted(weekly_totals.items())
    labels = [week.strftime('%Y-%m-%d') for week, total in sorted_weekly_totals]
    data = [float(total) for week, total in sorted_weekly_totals]

    return labels, data

def calculate_monthly_totals():
    reservations = Reservation.objects.all()
    monthly_totals = defaultdict(Decimal)

    for reservation in reservations:
        start_date = reservation.start_date
        if start_date:
            month = start_date.strftime('%Y-%m')
            monthly_totals[month] += reservation.total_amount()

    sorted_monthly_totals = sorted(monthly_totals.items())
    labels = [month for month, total in sorted_monthly_totals]
    data = [float(total) for month, total in sorted_monthly_totals]

    return labels, data

def calculate_yearly_totals():
    reservations = Reservation.objects.all()
    yearly_totals = defaultdict(Decimal)

    for reservation in reservations:
        start_date = reservation.start_date
        if start_date:
            year = start_date.year
            yearly_totals[year] += reservation.total_amount()

    sorted_yearly_totals = sorted(yearly_totals.items())
    labels = [str(year) for year, total in sorted_yearly_totals]
    data = [float(total) for year, total in sorted_yearly_totals]

    return labels, data



@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def stats(request):
    weekly_labels, weekly_data = calculate_weekly_totals()
    monthly_labels, monthly_data = calculate_monthly_totals()
    yearly_labels, yearly_data = calculate_yearly_totals()
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    spends = Spend.objects.all()
    final_amount = calculate_final_amount(spends)




    context = {
        'cars': Car.objects.all(),
        'allcars': Car.objects.filter(availability=True).count(),
        'car_rented': Car.objects.filter(status='rented').count(),
        'car_available': Car.objects.filter(status='available').count(),
        'car_broke': Car.objects.filter(status='broke').count(),
        'car_unavailable': Car.objects.filter(status='unavailable').count(),
        'reservations': Reservation.objects.all(),
        'allreservations': Reservation.objects.filter(availability=True).count(),
        'reservation_active': Reservation.objects.filter(status='active').count(),
        'reservation_ended': Reservation.objects.filter(status='ended').count(),
        'clients': Client.objects.all(),
        'allclients': Client.objects.filter(availability=True).count(),
        'workers': Worker.objects.all(),
        'allworkers': Worker.objects.filter(availability=True).count(),
        'total_amount': calculate_total_amount(),
        'weekly_labels': weekly_labels,
        'weekly_data': weekly_data,
        'monthly_labels': monthly_labels,
        'monthly_data': monthly_data,
        'yearly_labels': yearly_labels,
        'yearly_data': yearly_data,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
        'final_amount': final_amount,
    }

    return render(request, 'pages/stats.html', context)
###################### Workers ######################
@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def worker_view(request, id):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    worker_id = Worker.objects.get(id=id)
    entry_spends = Spend.objects.filter(entry_worker=worker_id).order_by('-created_at')
    expense_spends = Spend.objects.filter(expense_worker=worker_id).order_by('-created_at')
    recent_spends = list(entry_spends) + list(expense_spends)
    recent_spends.sort(key=lambda spend: spend.created_at, reverse=True)
    if request.method == 'post':
        worker_save = WorkerForm(request.POST, request.FILES, instance=worker_id)
        if worker_save.is_valid():
            worker_save.save()
            return HttpResponseRedirect(reverse('workers'))
    else:
        worker_save = WorkerForm(instance=worker_id)

    

    context = {
        'worker': Worker.objects.all().order_by('-created_at'),
        'form': worker_save,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
        'recent_spends': recent_spends,
    }

    return render(request, 'pages/worker-view.html', context)


###################### Logs ######################
@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def history(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    logs = UserActionLog.objects.all().order_by('-timestamp')

    

    context = {
        'logs': logs,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
        }
    return render(request, 'pages/history.html', context)




@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def spends_add(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    if request.method == 'POST':
        add_spend = SpendForm(request.POST)
        if add_spend.is_valid():
            add_spend.save()
            # Log the action
            UserActionLog.objects.create(
                user=request.user,
                action='add',
                description=f"Added Spend"
            )
        return HttpResponseRedirect(reverse('spends'))
    
    
    
    context = {
        'form': SpendForm(),
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/spends-add.html', context)


@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def spends(request):

    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    
   


    context = {
        'spends': Spend.objects.all().order_by('-created_at'),
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/spends.html', context)

@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def spends_delete(request, id):
    spends_delete = get_object_or_404(Spend, id=id)
    if request.method == 'POST':
        spends_delete.delete()
        # Log the action
        UserActionLog.objects.create(
            user=request.user,
            action='Delete',
            description=f"Delete Spend"
        )
        return redirect('/spends')
    
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    
    
    
    context = {
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
        
    return render(request, 'pages/spends-delete.html', context)

@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def spends_edit(request, id):
    spend_id = Spend.objects.get(id=id)
    if request.method == 'POST':
        add_spend = SpendForm(request.POST, instance=spend_id)
        if add_spend.is_valid():
            add_spend.save()
            # Log the action
            UserActionLog.objects.create(
                user=request.user,
                action='Update',
                description=f"Update Spend"
            )
        return HttpResponseRedirect(reverse('spends'))
    else:
        add_spend = SpendForm(instance=spend_id)

    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    
    
    
    context = {
        'form': add_spend,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/spends-edit.html', context)









@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def invoice_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    
    
    context = {
        'reservation': reservation,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/invoice.html', context)














def search(request):
    query = request.GET.get('q')
    if query:
        cars = Car.objects.filter(Q(model__icontains=query) | Q(matricule__icontains=query))
        clients = Client.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        reservations = Reservation.objects.filter(
            Q(client__first_name__icontains=query) | Q(client__last_name__icontains=query) |
            Q(car__model__icontains=query) | Q(car__matricule__icontains=query)
        )
        spends = Spend.objects.filter(Q(entry_date__icontains=query) | Q(expense_date__icontains=query))
    else:
        cars = Car.objects.none()
        clients = Client.objects.none()
        reservations = Reservation.objects.none()
        spends = Spend.objects.none()

    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    

    context = {
        'query': query,
        'cars': cars,
        'clients': clients,
        'reservations': reservations,
        'spends': spends,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/search-results.html', context)

























































@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def custom_invoices(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            # Log the action
            UserActionLog.objects.create(
                user=request.user,
                action='Create',
                description=f"Create Custom Invoice"
            )
            return redirect('printinvoice', invoice_id=invoice.id)
    else:
        form = InvoiceForm()

    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    
    
        
    context = {
        'notifications': notifications,
        'unread_notifications': unread_notifications,
        'form': form,
    }
    
    return render(request, 'pages/create-invoices.html', context)

def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    total_amount = invoice.total_amount()
    total_after_discount = total_amount - invoice.discount

    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    
    
    
    context = {
        'invoice': invoice,
        'total_after_discount': total_after_discount,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }

    return render(request, 'pages/print-invoice.html', context)

def pdf_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    total_amount = invoice.total_amount()  # Call the method
    total_after_discount = total_amount - invoice.discount
    return render(request, 'pages/pdf-invoice.html', {'invoice': invoice, 'total_after_discount': total_after_discount})





def pdf_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    total_amount = reservation.total_amount()  # Call the method
    return render(request, 'pages/pdf-reservation-invoice.html', {'reservation': reservation, 'total_amount': total_amount})

















@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def cars_maintenance(request):
    form = MaintenanceForm()
    maintenances = Maintenance.objects.all().order_by('-created_at')
    if request.method =='POST':
        add_maintenance = MaintenanceForm(request.POST)
        if add_maintenance.is_valid():
            add_maintenance.save()
            # Log the add action
            UserActionLog.objects.create(
                user=request.user,
                action='add',
                description=f"Added Maintenance for: {maintenances.car}"
            )
            return redirect('/maintenance')
    
    for maintenance in maintenances:
        latest_reservation = Reservation.objects.filter(car=maintenance.car).order_by('-end_date').first()
        if latest_reservation:
            maintenance.end_mileage = latest_reservation.end_mileage
        else:
            maintenance.end_mileage = 0  # or some default value if there's no reservation
        
        
    
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    
    

    context = {
        'form': form,
        'maintenance': maintenances,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/cars-maintenance.html', context)
@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def maintenance_delete(request, id):
    maintenance_delete = get_object_or_404(Maintenance, id=id)
    if request.method == 'POST':
        maintenance_delete.delete()
        # Log the add action
        UserActionLog.objects.create(
            user=request.user,
            action='Delete',
            description=f"Delete {maintenance_delete.car} Maintenance"
        )


        return redirect('/maintenance')
    
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    
    
    context = {
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    
    return render(request, 'pages/maintenance-delete.html', context)
@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def maintenance_edit(request, id):
    maintenance_id = Maintenance.objects.get(id=id)
    if request.method == 'POST':
        maintenance_save = MaintenanceForm(request.POST, instance=maintenance_id)
        if maintenance_save.is_valid():
            maintenance_save.save()
            # Log the add action
            UserActionLog.objects.create(
            user=request.user,
            action='Update',
            description=f"Update Maintenance for: {maintenance_id.car} "
        )
            return HttpResponseRedirect(reverse('cars_maintenance'))
            
    else:
        maintenance_save = MaintenanceForm(instance=maintenance_id)

    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)   
    

    context = {
        'form': maintenance_save,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/maintenance-edit.html', context)