from Apps.Common.Helpers.ErrorHandling.Exceptions import *
from Apps.Common.Repositories.FileManager import FileManager

class MatrixDimensionsOperations:
    path = "Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    def __init__(self):
        try:
            pass
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, "MatrixDimensionsOperations.__init__")
            raise

    def determineDimensionsOfAddition(self, matrix1_dims, matrix2_dims):
        try:
            rows1, cols1 = matrix1_dims
            rows2, cols2 = matrix2_dims

            if rows1 != rows2 or cols1 != cols2:

                raise ImposibleMatrixOperation(
                    f"""
            Error: La operación de suma matricial no es posible.
            Sean A ∈ R^({rows1}x{cols1}) ∧ B ∈ R^({rows2}x{cols2})
            A + B está definida ⟺ dim(A) = dim(B)
            En este caso, (({rows1}x{cols1}) ≠ ({rows2}x{cols2}))
            ∴ A + B no está definida

            """
                )

            return (rows1, cols1)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix1_dims: {matrix1_dims}, matrix2_dims: {matrix2_dims}")
            raise

    def determineDimensionsOfSubstraction(self, matrix1Dims, matrix2Dims):
        try:
            rows1, cols1 = matrix1Dims
            rows2, cols2 = matrix2Dims
            if rows1 != rows2 or cols1 != cols2:

                raise ImposibleMatrixOperation(
                    f"""
            Error: La operación de resta matricial no es posible.
            Sean A ∈ R^({rows1}x{cols1}) ∧ B ∈ R^({rows2}x{cols2})
            A - B está definida ⟺ dim(A) = dim(B)
            En este caso, (({rows1}x{cols1}) ≠ ({rows2}x{cols2}))
            ∴ A - B no está definida

            """
                )
            return (rows1, cols1)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix1Dims: {matrix1Dims}, matrix2Dims: {matrix2Dims}")
            raise

    def determineDimensionsOfMultiplication(self, matrix1Dims, matrix2Dims):
        try:
            if isinstance(matrix1Dims, tuple) and isinstance(matrix2Dims, int):
                return matrix1Dims
            
            rows1, cols1 = matrix1Dims
            rows2, cols2 = matrix2Dims
            if cols1 != rows2:
                raise ImposibleMatrixOperation(
                    f"""
            Error: La operación de multiplicación matricial no es posible.
            Sean A ∈ R^({rows1}x{cols1}) ∧ B ∈ R^({rows2}x{cols2})
            A * B está definida ⟺ columnas(A) = filas(B)
            En este caso, ({cols1} ≠ {rows2})
            ∴ A * B no está definida

            """
                )
            return (rows1, cols2)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix1Dims: {matrix1Dims}, matrix2Dims: {matrix2Dims}")
            raise