import numpy as np
from Apps.Common.Repositories.FileManager import FileManager

class MatrixValidator:
    path = "Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def canAddOrSubtract(self, matrix_a, matrix_b):
        try:
            return matrix_a.shape == matrix_b.shape
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix_a: {matrix_a}, matrix_b: {matrix_b}")
            return None

    def canMultiply(self, matrix_a, matrix_b):
        try:
            return matrix_a.shape[1] == matrix_b.shape[0]
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix_a: {matrix_a}, matrix_b: {matrix_b}")
            return None

    def can_transpose(self, matrix):
        try:
            return True
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix: {matrix}")
            return None

    def canInvert(self, matrix):
        try:
            return matrix.shape[0] == matrix.shape[1] and not np.isclose(
                np.linalg.det(matrix), 0
            )
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix: {matrix}")
            return None