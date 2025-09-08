from django.urls import path
from .views import randomGraph, process_and_save_iterations

urlpatterns = [
    # Ruta para la funcionalidad original de las entregas anteriores
    path("randomGraph/", randomGraph, name="randomGraph"),
    
    # Ruta para la NUEVA funcionalidad de procesamiento iterativo y guardado en BD
    path("process/", process_and_save_iterations, name="process_iterations"),
]

