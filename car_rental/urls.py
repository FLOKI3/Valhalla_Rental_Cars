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
    path('maintenance', views.cars_maintenance, name='cars_maintenance'),
    path('maintenance-delete/<int:id>', views.maintenance_delete, name='maintenance_delete'),
    path('maintenance-edit/<int:id>', views.maintenance_edit, name='maintenance_edit'),
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

    path('spends-add/', views.spends_add, name='spends_add'),
    path('spends', views.spends, name='spends'),
    path('spend-delete/<int:id>', views.spends_delete, name='spends_delete'),
    path('spend-edit/<int:id>', views.spends_edit, name='spends_edit'),



    

    
    

    path('invoice/<int:reservation_id>', views.invoice_view, name='invoice'),

    path('custom-invoices/', views.custom_invoices, name='custom_invoices'),
    path('print-invoice/<int:invoice_id>/', views.print_invoice, name='printinvoice'),
    path('invoice/print/<int:invoice_id>/', views.pdf_invoice, name='pdfinvoice'),



    path('reservation/print/<int:reservation_id>/', views.pdf_reservation, name='pdf_reservation'),

    
]
