from django.contrib import admin
from .models import IterationRun, DataPoint

# Registramos los nuevos modelos para que aparezcan en el panel de administración.
admin.site.register(IterationRun)
admin.site.register(DataPoint)