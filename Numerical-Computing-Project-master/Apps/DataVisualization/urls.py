from django.urls import path
# Importamos los nombres de función correctos desde views.py
from .views import randomGraph, process_and_save_iterations_m2m

urlpatterns = [
    # Ruta para la funcionalidad original
    path("randomGraph/", randomGraph, name="randomGraph"),
    
    # Ruta para la NUEVA funcionalidad, apuntando al nombre de función correcto
    path("process-m2m/", process_and_save_iterations_m2m, name="process_iterations_m2m"),
]