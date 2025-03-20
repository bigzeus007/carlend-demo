"""
URL configuration for carlend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from home.views import home

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('vehicles/', include('vehicles.urls')),  # Inclure les URLs de l'application
    path('reservations/', include('reservations.urls')),
    path('home/', include('home.urls')),  # Page d'accueil
    path('', home, name='home'),  # Associer l'URL racine à la vue d'accueil
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Ajout de l'URL de connexion
    path('parc/', include('parc.urls')),  # Ajout de l'application Parc
    path('historiques/', include('historiques.urls')),
    # Ajout dModification mdp
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('password_change/', login_required(auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html')), name='password_change'),
    path('password_change/done/', login_required(auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html')), name='password_change_done'),
]
# Ajoutez ceci pour inclure les fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)