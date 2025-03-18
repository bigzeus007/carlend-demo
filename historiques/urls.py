from django.urls import path
from . import views

urlpatterns = [
    path('', views.historique_index, name='historique_index'),
    path('pret/', views.historique_pret, name='historique_pret'),
    path('annulation/', views.historique_annulation, name='historique_annulation'),
    
]

