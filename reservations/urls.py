from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('add/', login_required(views.add_reservation), name='add_reservation'),
    path('<int:pk>/edit/', views.edit_reservation, name='edit_reservation'),
    path('<int:pk>/assign/', views.assign_vehicle, name='assign_vehicle'),
    path('history/', views.reservation_history, name='reservation_history'),
    path('<int:pk>/details/', views.reservation_detail, name='reservation_detail'),
    path('<int:pk>/validate/', login_required(views.validate_reservation), name='validate_reservation'),
    path('<int:pk>/archive/', views.archive_reservation, name='archive_reservation'),

]
