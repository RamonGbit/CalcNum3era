import numpy as np


class MatrixValidator:
    def canAddOrSubtract(self, matrix_a, matrix_b):
        return matrix_a.shape == matrix_b.shape

    def canMultiply(self, matrix_a, matrix_b):
        return matrix_a.shape[1] == matrix_b.shape[0]

    def can_transpose(self, matrix):
        return True

    def canInvert(self, matrix):
        return matrix.shape[0] == matrix.shape[1] and not np.isclose(
            np.linalg.det(matrix), 0
        )


class DataValidator:
    def canCalculateLinearRegression(self, x_values, y_values):
        """Valida si se puede calcular regresión lineal con los datos dados"""
        x = np.array(x_values, dtype=float)
        y = np.array(y_values, dtype=float)
        
        # Verificar que tengan la misma longitud
        if len(x) != len(y):
            return False
        
        # Verificar que no estén vacíos
        if len(x) == 0:
            return False
        
        # Verificar que tengan al menos 2 puntos
        if len(x) < 2:
            return False
        
        # Verificar que no todos los valores de X sean iguales
        if np.all(x == x[0]):
            return False
        
        return True
