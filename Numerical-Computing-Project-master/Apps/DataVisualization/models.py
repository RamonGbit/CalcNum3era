from django.db import models

class PlotResult(models.Model):
    point1X = models.FloatField(help_text="X component of the first point/vector.")
    point1Y = models.FloatField(help_text="Y component of the first point/vector.")
    point1Z = models.FloatField(help_text="Z component of the first point/vector.")

    point2X = models.FloatField(help_text="X component of the second point/vector.")
    point2Y = models.FloatField(help_text="Y component of the second point/vector.")
    point2Z = models.FloatField(help_text="Z component of the second point/vector.")

    point3X = models.FloatField(help_text="X component of the third point/vector.")
    point3Y = models.FloatField(help_text="Y component of the third point/vector.")
    point3Z = models.FloatField(help_text="Z component of the third point/vector.")

    relativeError = models.FloatField(help_text="Relative error in this iteration.")

    def __str__(self):
        return (f"Plot Result: P1[{self.point1X:.2f},{self.point1Y:.2f},{self.point1Z:.2f}], "
                f"P2[{self.point2X:.2f},{self.point2Y:.2f},{self.point2Z:.2f}], "
                f"P3[{self.point3X:.2f},{self.point3Y:.2f},{self.point3Z:.2f}] "
                f"- Relative Error: {self.relativeError:.2f}")

    class Meta:
        verbose_name = "Plot Result"
        verbose_name_plural = "Plot Results"
        ordering = ['-id'] 