from django.urls import path
from . import views

urlpatterns = [

    # Dashboard general
    path(
        'dashboard/',
        views.DashboardView.as_view(),
        name='dashboard'
    ),

    # Datos sensores
    path(
        'datos/',
        views.DatosView.as_view(),
        name='datos'
    ),

    # Alertas
    path(
        'alertas/',
        views.AlertasView.as_view(),
        name='alertas'
    ),

    # Dispositivos
    path(
        'dispositivos/',
        views.DispositivosView.as_view(),
        name='dispositivos'
    ),

    # Historial
    path(
        'historial/',
        views.HistorialView.as_view(),
        name='historial'
    ),

]