from django.urls import path
from . import views
from django.http import HttpResponseForbidden

def read_only_view(request, *args, **kwargs):
    return HttpResponseForbidden("Cette démo est en lecture seule.")

urlpatterns = [
    # Vue par défaut path('', views.index, name='index'),  
    path('', views.vehicle_list, name='vehicle_list'),
    path('add/', views.add_vehicle,read_only_view, name='add_vehicle'),
    path('<int:pk>/edit/', views.edit_vehicle,read_only_view, name='edit_vehicle'),
    path('<int:pk>/delete/', views.delete_vehicle,read_only_view, name='delete_vehicle'),
    # path('<int:pk>/detail/', views.vehicle_detail, name='vehicle_detail'),
]
