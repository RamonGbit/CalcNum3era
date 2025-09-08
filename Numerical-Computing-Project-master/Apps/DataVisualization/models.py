from django.db import models

class IterationRun(models.Model):
    """
    Representa una única ejecución o iteración del análisis.
    """
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que se registró la iteración."
    )

    class Meta:
        verbose_name = "Corrida de Iteración"
        verbose_name_plural = "Corridas de Iteraciones"
        ordering = ['-timestamp'] 

    def __str__(self):
        return f"Iteración registrada el {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class DataPoint(models.Model):
    """
    Representa un único punto de datos (X, Y) perteneciente a una iteración.
    """
    iteration_run = models.ForeignKey(
        IterationRun,
        related_name='data_points',
        on_delete=models.CASCADE,
        help_text="La corrida de iteración a la que pertenece este punto."
    )
    x_value = models.IntegerField(help_text="Coordenada X del punto.")
    y_value = models.IntegerField(help_text="Coordenada Y del punto.")

    class Meta:
        verbose_name = "Punto de Dato"
        verbose_name_plural = "Puntos de Datos"

    def __str__(self):
        return f"({self.x_value}, {self.y_value})"

