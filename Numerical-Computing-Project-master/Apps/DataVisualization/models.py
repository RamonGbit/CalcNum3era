from django.db import models

class Punto(models.Model):
    coordenada_x = models.IntegerField()
    coordenada_y = models.IntegerField()

    class Meta:
        unique_together = ('coordenada_x', 'coordenada_y')

    def __str__(self):
        return f"({self.coordenada_x}, {self.coordenada_y})"

class Iteracion(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    puntos = models.ManyToManyField(Punto, related_name="iteraciones")
    cantidad_errores = models.IntegerField(default=0)
    grafica_image = models.ImageField(upload_to='graficas/', blank=True, null=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Iteración del {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"