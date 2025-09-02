
from Apps.Common.Helpers.ErrorHandling.Exceptions import *

class MatrixDimensionsOperations:

    def __init__(self):
        pass

    def determineDimensionsOfAddition(self, matrix1_dims, matrix2_dims):
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

    def determineDimensionsOfSubstraction(self, matrix1Dims, matrix2Dims):
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

    def determineDimensionsOfMultiplication(self, matrix1Dims, matrix2Dims):
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

