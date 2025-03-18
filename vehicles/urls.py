from django.urls import path
from . import views

urlpatterns = [
    # Vue par défaut path('', views.index, name='index'),  
    path('', views.vehicle_list, name='vehicle_list'),
    path('add/', views.add_vehicle, name='add_vehicle'),
    path('<int:pk>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('<int:pk>/delete/', views.delete_vehicle, name='delete_vehicle'),
    # path('<int:pk>/detail/', views.vehicle_detail, name='vehicle_detail'),
]
