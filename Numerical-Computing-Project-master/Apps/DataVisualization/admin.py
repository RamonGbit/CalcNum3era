from django.contrib import admin
from .models import Punto, Iteracion

# Registramos los nuevos modelos para que aparezcan en el panel de administración.
admin.site.register(Punto)
admin.site.register(Iteracion)