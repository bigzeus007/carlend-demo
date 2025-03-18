from django.urls import path
from . import views

urlpatterns = [
    path('', views.parc_list, name='parc_list'),
    path('<int:pk>/info/', views.parc_info, name='parc_info'),
    path('<int:pk>/detail/', views.vehicle_info, name='vehicle_info'),
    path('<int:pk>/update-status/', views.parc_update, name='parc_update'),
    path('<int:pk>/contrat/', views.generate_contract, name='generate_contract'),
    path('<int:pk>/confirm-return/', views.confirm_return_update, name='confirm_return_update'),

]
