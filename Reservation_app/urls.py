from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # login + logout + register

    path('register/', views.register, name='register'),
    path('', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    # Admin urls -----------------------------------------------------------------------------------

    path('admin/home/', views.home_a, name='home'),
    path('admin/home_stati/', views.home_stati, name='home_stati'),
    path('admin/client/', views.client_a, name='clients'),


    path('admin/client_info/<str:pk_test>/', views.view_a_c, name='view_a_c'),
    path('admin/event_info/<str:pk_test>/', views.view_a_e, name='view_a_e'),
    path('admin/createClient/', views.create_client, name='create_client'),
    path('admin/updateClient/<str:pk>/', views.update_client, name='update_client'),
    path('admin/deleteClient/<str:pk>/', views.delete_client, name='delete_client'),
    # Event
    path('admin/event/', views.event_a, name='events_a'),
    path('admin/add_event/', views.add_event_a, name='add_event_a'),
    path('admin/delete_event/<str:pk>/', views.delete_event_a, name='delete_event_a'),
    path('admin/update_event/<str:pk>/', views.update_event_a, name='update_event_a'),
    path('admin/Valider/<str:pk>/', views.validation, name='validation'),
    # les nouveaux urls
    path('Admin/home/events', views.search_events_a, name='search_events_a'),
    path('organiseur/setting/', views.setting_organisuer, name='setting_organisuer'),

    # organiseur urls -----------------------------------------------------------------------------------
    path('organiseur/home/', views.home_o, name='home_o'),
    path('organiseur/event/', views.event_o, name='events_o'),
    path('organiseur/reservation/', views.clients_reservation, name='clients_reservation'),
    path('organiseur/event_info/<str:pk_test>/', views.view_o_e, name='view_o_e'),
    path('organiseur/delete_event/<str:pk>/', views.delete_event, name='delete_event'),
    path('organiseur/update_event/<str:pk>/', views.update_event, name='update_event'),
    path('organiseur/add_event/', views.add_event, name='add_event'),
    path('organiseur/statistique/', views.statistique_org, name='statistique_org'),


    # Client urls -----------------------------------------------------------------------------------

    path('client/home/', views.home_c, name='home_client'),
    path('client/notifications/', views.notifications, name='notifications'),
    path('client/home/search', views.search_events, name='search_events'),
    path('client/fistivals/', views.event_festival, name='fistivals'),
    path('client/spectacles/', views.event_spectacle, name='spectacles'),
    path('client/sports/', views.event_sport, name='sports'),
    path('client/conférences/', views.event_conférence, name='conférences'),
    path('client/buy/<str:pk>/', views.buy_c, name='buy'),
    path('client/panel/', views.panel, name='panel'),
    path('client/carde/<str:pk>/', views.carde_autentification, name='carde_autentification'),




]