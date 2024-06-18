from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CarForm, ClientForm, ReservationForm, WorkerForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.db.models import Sum, Q
from datetime import datetime, date, timedelta
from collections import defaultdict

from car_rental.calculation import calculate_total_amount

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
    context = {
        'category': Category.objects.all(),
        'cars': Car.objects.all().order_by('-created_at'),
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
    if request.method == 'POST':
        car_save = CarForm(request.POST, request.FILES, instance=car_id)
        if car_save.is_valid():
            car =car_save.save()
            # Log the edit action
            UserActionLog.objects.create(
                user=request.user,
                action='update',
                description=f"Updated car: {car.model} with Registration N°: {car.matricule}"
            )
            return HttpResponseRedirect(reverse('cars'))
    else:
        car_save = CarForm(instance=car_id)

    context = {
        'form': car_save,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/car-edit.html', context)
@login_required
def car_cards(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    context = {
        'cars': Car.objects.all().order_by('-created_at'),
        'form': CarForm(),
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'pages/cars-card.html', context)
@login_required
def car_detail(request, id):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    context = {
        'car': get_object_or_404(Car, id=id),
        'notifications': notifications,
        'unread_notifications': unread_notifications,        
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
    context = {
        'clients': Client.objects.all().order_by('-created_at'),
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
            
            return HttpResponseRedirect('/reservations')
    
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
    }

    return render(request, 'pages/stats.html', context)
###################### Workers ######################
@login_required
@permission_required('car_rental.can_view_cars', raise_exception=False)
def worker_view(request, id):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    worker_id = Worker.objects.get(id=id)
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





































def search(request):
    query = request.GET.get('q')
    if query:
        cars = Car.objects.filter(Q(model__icontains=query) | Q(matricule__icontains=query))
        clients = Client.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        reservations = Reservation.objects.filter(
            Q(client__first_name__icontains=query) | Q(client__last_name__icontains=query) |
            Q(car__model__icontains=query) | Q(car__matricule__icontains=query)
        )
    else:
        cars = Car.objects.none()
        clients = Client.objects.none()
        reservations = Reservation.objects.none()

    context = {
        'query': query,
        'cars': cars,
        'clients': clients,
        'reservations': reservations,
    }
    return render(request, 'pages/search-results.html', context)

