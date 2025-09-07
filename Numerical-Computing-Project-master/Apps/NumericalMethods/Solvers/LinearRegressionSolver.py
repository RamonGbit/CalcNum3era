import numpy as np
from Apps.NumericalMethods.utils import DataValidator
from Apps.Common.Helpers.ErrorHandling.Exceptions import *


class LinearRegressionSolver:
    def __init__(self):
        self.validator = DataValidator()

    def calculateLinearRegression(self, x_values, y_values):
        """
        Calcula la recta de mejor ajuste usando el método de mínimos cuadrados.
        
        Args:
            x_values (array-like): Array de valores de X
            y_values (array-like): Array de valores de Y
            
        Returns:
            dict: Diccionario con 'slope' (pendiente) y 'intercept' (intercepto)
            
        Raises:
            NumberIsInvalid: Si los datos no son válidos para regresión lineal
        """
        # Validar los datos de entrada
        if not self.validator.canCalculateLinearRegression(x_values, y_values):
            raise NumberIsInvalid("Los datos proporcionados no son válidos para calcular regresión lineal")
        
        # Convertir a arrays de numpy
        x = np.array(x_values, dtype=float)
        y = np.array(y_values, dtype=float)
        
        # Calcular las medias
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        # Calcular la pendiente usando mínimos cuadrados
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)
        
        slope = numerator / denominator
        
        # Calcular el intercepto
        intercept = y_mean - slope * x_mean
        
        return {
            'slope': slope,
            'intercept': intercept
        }
