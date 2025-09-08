import numpy as np
from Apps.NumericalMethods.utils import MatrixValidator
from Apps.Common.Helpers.ErrorHandling.Exceptions import *
from Apps.Common.Repositories.FileManager import FileManager

class MatrixOperations:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self):
        try:
            self.validator = MatrixValidator()
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, "MatrixOperations.__init__")
            raise

    def add(self, matrixA:np.ndarray, matrixB:np.ndarray):
        try:
            if not self.validator.canAddOrSubtract(matrixA, matrixB):
                raise ValueError("Las matrices no tienen las mismas dimensiones")

            result = np.zeros((matrixA.shape[0], matrixA.shape[1]))
            for i in range(matrixA.shape[0]):
                for j in range(matrixA.shape[1]):
                    result[i, j] = matrixA[i, j] + matrixB[i, j]
            return result
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrixA_shape: {matrixA.shape}, matrixB_shape: {matrixB.shape}")
            raise

    def subtract(self, matrixA:np.ndarray, matrixB:np.ndarray):
        try:
            if not self.validator.canAddOrSubtract(matrixA, matrixB):
                raise ValueError("Las matrices no tienen las mismas dimensiones")

            result = np.zeros((matrixA.shape[0], matrixA.shape[1]))
            for i in range(matrixA.shape[0]):
                for j in range(matrixA.shape[1]):
                    result[i, j] = matrixA[i, j] - matrixB[i, j]
            return result
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrixA_shape: {matrixA.shape}, matrixB_shape: {matrixB.shape}")
            raise

    def multiply(self, a, b):
        try:
            if isinstance(a, (int, float)) and isinstance(b, np.ndarray):
                return self.scalarMultiply(b, a)
            if isinstance(a, np.ndarray) and isinstance(b, (int, float)):
                return self.scalarMultiply(a, b)
            if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
                return self.multiplyMatrix(a, b)
            else:
                raise ValueError("Error: Se han ingresado objetos inválidos")
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"a_type: {type(a)}, b_type: {type(b)}")
            raise
        
    def multiplyMatrix(self, matrixA:np.ndarray, matrixB:np.ndarray):
        try:
            if not self.validator.canMultiply(matrixA, matrixB):
                raise ValueError("Número de columnas de A debe coincidir con filas de B")

            result = np.zeros((matrixA.shape[0], matrixB.shape[1]))
            for i in range(matrixA.shape[0]):
                for j in range(matrixB.shape[1]):
                    sum_val = 0
                    for k in range(matrixA.shape[1]):
                        sum_val += matrixA[i, k] * matrixB[k, j]
                    result[i, j] = sum_val
            return result
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrixA_shape: {matrixA.shape}, matrixB_shape: {matrixB.shape}")
            raise

    def scalarMultiply(self, matrix:np.ndarray, scalar:int):
        try:
            result = np.zeros((matrix.shape[0], matrix.shape[1]))
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    result[i, j] = matrix[i, j] * scalar
            return result
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix_shape: {matrix.shape}, scalar: {scalar}")
            raise

    def transpose(self, matrix:np.ndarray):
        try:
            result = np.zeros((matrix.shape[1], matrix.shape[0]))
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    result[j, i] = matrix[i, j]
            return result
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix_shape: {matrix.shape}")
            raise

    def inverse(self, matrix:np.ndarray):
        try:
            if not self.validator.canInvert(matrix):
                raise ValueError("Matriz no es cuadrada o es singular")

            n = matrix.shape[0]
            det = self.validator._determinant(matrix)

            if n == 1:
                return np.array([[1 / matrix[0, 0]]])
            cofactors = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                    cofactor = (-1) ** (i + j) * self.validator._determinant(minor)
                    cofactors[i, j] = cofactor

            adjugate = self.transpose(cofactors)

            inverse = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    inverse[i, j] = adjugate[i, j] / det

            return inverse
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix_shape: {matrix.shape}, matrix_det: {np.linalg.det(matrix) if matrix.shape[0] == matrix.shape[1] else 'N/A'}")
            raise