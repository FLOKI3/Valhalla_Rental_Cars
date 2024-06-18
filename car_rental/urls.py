from django.urls import path
from . import views


urlpatterns = [
    # Dashboard
    # Cars
    path('cars', views.cars, name='cars'),
    path('car-cards', views.car_cards, name='car_cards'),
    path('car-detail/<int:id>', views.car_detail, name='car_detail'),
    path('car-delete/<int:id>', views.car_delete, name='car_delete'),
    path('car-edit/<int:id>', views.car_edit, name='car_edit'),
    # Clients
    path('clients', views.clients, name='clients'),
    path('client-profile-delete', views.client_profile_delete, name='client_profile_delete'),
    path('client-edit/<int:id>', views.client_edit, name='client_edit'),
    path('client-delete/<int:id>', views.client_delete, name='client_delete'),
    # Reservations
    path('reservations', views.reservations, name='reservations'),
    path('reservation-edit/<int:id>', views.reservation_edit, name='reservation_edit'),
    path('reservation-delete/<int:id>', views.reservation_delete, name='reservation_delete'),
    # Stats
    path('dashboard', views.stats, name='stats'),
    # Workers
    path('workers', views.users_list, name='workers'),
    path('worker-view/<int:id>', views.worker_view, name='worker_view'),
    # History
    path('history', views.history, name='history'),



    path('', views.login_view, name='login'),
    path('', views.logout_view, name='logout'),
    
    
    
    path('search/', views.search, name='search'),



    
    
    
    
    
    

    
    
    
    
    

    

    
]
