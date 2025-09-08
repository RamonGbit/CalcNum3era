from Apps.Common.Helpers.ErrorHandling.Exceptions import *
import numpy as np
from Apps.Common.Repositories.FileManager import FileManager

class SystemOfEquationsSolver:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    def __init__(self):
        try:
            self.methodsToSolveSystem = {
                "Gauss-Jordan con pivoteo parcial": self.gaussJordanPartialPivoting,
                "Gauss-Jordan con pivoteo escalonado": self.gaussJordanStaggeredPivoting,
                "Gauss-Jordan con pivoteo completo": self.gaussJordanFullPivoting,
                "Gauss-Seidel": self.gaussSeidel,
            }
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, "SystemOfEquationsSolver.__init__")
            raise

    def gaussJordanPartialPivoting(
        self, coefficients: np.ndarray, independents: np.ndarray
    ) -> np.ndarray:
        try:
            coefficientsColumns = len(coefficients)
            augmentedMatrix = self.concatenateMatrixAndVector(coefficients, independents)

            for column in range(coefficientsColumns):
                maxRow = column
                for k in range(column + 1, coefficientsColumns):
                    if abs(augmentedMatrix[k, column]) > abs(
                        augmentedMatrix[maxRow, column]
                    ):
                        maxRow = k
                augmentedMatrix[[column, maxRow]] = augmentedMatrix[[maxRow, column]]

                pivot = augmentedMatrix[column, column]
                if pivot == 0:
                    raise SystemDontHaveSolution(
                        "Error: La matriz es singular y no puede resolverse."
                    )

                augmentedMatrix[column, column:] /= pivot

                for k in range(coefficientsColumns):
                    if k != column:
                        factor = augmentedMatrix[k, column]
                        augmentedMatrix[k, column:] -= (
                            factor * augmentedMatrix[column, column:]
                        )

            return augmentedMatrix[:, -1]
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"coefficients_shape: {coefficients.shape}, independents_shape: {independents.shape}")
            raise

    def gaussJordanStaggeredPivoting(
        self, coefficients: np.ndarray, independents: np.ndarray
    ) -> np.ndarray:
        try:
            if not isinstance(coefficients, np.ndarray) or not isinstance(
                independents, np.ndarray
            ):
                raise ValueError("Error: Has ingresado una matriz inválida")

            coefficientsColumns = len(coefficients[0])
            augmentedMatrix = self.concatenateMatrixAndVector(coefficients, independents)
            scalingFactors = self.searchScalingFactorsIn(coefficients)

            for pivotColumn in range(coefficientsColumns):
                pivotRow = pivotColumn
                maxRatioRow = pivotRow
                maxRatio = (
                    abs(augmentedMatrix[maxRatioRow][pivotColumn])
                    / scalingFactors[maxRatioRow]
                )

                for indexRow in range(pivotRow + 1, len(augmentedMatrix)):
                    ratio = (
                        abs(augmentedMatrix[indexRow][pivotColumn])
                        / scalingFactors[indexRow]
                    )
                    if ratio > maxRatio:
                        maxRatio = ratio
                        maxRatioRow = indexRow

                if maxRatioRow != pivotRow:
                    augmentedMatrix[[pivotRow, maxRatioRow]] = augmentedMatrix[
                        [maxRatioRow, pivotRow]
                    ]
                    scalingFactors[[pivotRow, maxRatioRow]] = scalingFactors[
                        [maxRatioRow, pivotRow]
                    ]

                pivot = augmentedMatrix[pivotRow][pivotColumn]

                if pivot == 0:
                    raise SystemDontHaveSolution(
                        "Error: El sistema de ecuaciones tiene soluciones infinitas o no tiene solución"
                    )

                for columna in range(pivotColumn, len(augmentedMatrix[pivotRow])):
                    augmentedMatrix[pivotRow][columna] /= pivot

                for indexRow in range(len(augmentedMatrix)):
                    if indexRow != pivotRow and augmentedMatrix[indexRow][pivotColumn] != 0:
                        valueToEliminate = augmentedMatrix[indexRow][pivotColumn]

                        for columna in range(pivotColumn, len(augmentedMatrix[pivotRow])):
                            augmentedMatrix[indexRow][columna] -= (
                                valueToEliminate * augmentedMatrix[pivotRow][columna]
                            )

            return augmentedMatrix[:, -1]
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"coefficients_shape: {coefficients.shape}, independents_shape: {independents.shape}")
            raise

    def gaussJordanFullPivoting(
        self, coefficients: np.ndarray, independents: np.ndarray
    ) -> np.ndarray:
        try:
            if not isinstance(coefficients, np.ndarray) or not isinstance(
                independents, np.ndarray
            ):
                raise ValueError("Error: Has ingresado una matriz inválida")

            coefficientsColumns = len(coefficients[0])
            augmentedMatrix = self.concatenateMatrixAndVector(coefficients, independents)
            positions = np.array(
                [i for i in range(1, coefficientsColumns + 1)], dtype=np.int8
            )

            for pivotColumn in range(coefficientsColumns):
                pivotRow = pivotColumn
                maxValuePosition = self.getMaxValuePosition(
                    coefficients[pivotRow:, pivotColumn:]
                )
                maxValuePosition[0] += pivotRow
                maxValuePosition[1] += pivotColumn

                if maxValuePosition[0] != pivotRow:
                    augmentedMatrix[[pivotRow, maxValuePosition[0]]] = augmentedMatrix[
                        [maxValuePosition[0], pivotRow]
                    ]

                if maxValuePosition[1] != pivotColumn:
                    augmentedMatrix[:, [pivotColumn, maxValuePosition[1]]] = (
                        augmentedMatrix[:, [maxValuePosition[1], pivotColumn]]
                    )
                    positions[[pivotColumn, maxValuePosition[1]]] = positions[
                        [maxValuePosition[1], pivotColumn]
                    ]

                pivot = augmentedMatrix[pivotRow][pivotColumn]

                if pivot == 0:
                    raise SystemDontHaveSolution(
                        "Error: El sistema de ecuaciones tiene soluciones infinitas o no tiene solución"
                    )

                for column in range(pivotColumn, len(augmentedMatrix[pivotRow])):
                    augmentedMatrix[pivotRow][column] /= pivot

                for row in range(len(augmentedMatrix)):
                    if row != pivotRow and augmentedMatrix[row][pivotColumn] != 0:
                        valueToEliminate = augmentedMatrix[row][pivotColumn]

                        for column in range(pivotColumn, len(augmentedMatrix[pivotRow])):
                            augmentedMatrix[row][column] -= (
                                valueToEliminate * augmentedMatrix[pivotRow][column]
                            )

            return self.sortResultByPosition(augmentedMatrix[:, -1], positions)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"coefficients_shape: {coefficients.shape}, independents_shape: {independents.shape}")
            raise

    def concatenateMatrixAndVector(
        self, matrix: np.ndarray, vector: np.ndarray
    ) -> np.ndarray:
        try:
            if not isinstance(matrix, np.ndarray) or not isinstance(vector, np.ndarray):
                raise ValueError("Error: Has ingresado una matriz inválida")

            concatenatedMatrix = np.zeros((len(matrix), len(matrix) + 1), dtype=np.float64)
            for i in range(len(matrix)):
                concatenatedMatrix[i][: len(matrix[i])] = matrix[i]
                concatenatedMatrix[i][-1] = vector[i]

            return concatenatedMatrix
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix_shape: {matrix.shape}, vector_shape: {vector.shape}")
            raise

    def searchScalingFactorsIn(self, matrix: np.ndarray) -> np.ndarray:
        try:
            if not isinstance(matrix, np.ndarray):
                raise ValueError("Error: Has ingresado una matriz inválida")

            scalingFactors = np.zeros(len(matrix), dtype=np.float64)
            for i in range(len(matrix)):
                maxValueColumn = 0
                for j in range(len(matrix[0])):
                    if abs(matrix[i][j]) > abs(matrix[i][maxValueColumn]):
                        maxValueColumn = j

                scalingFactors[i] = abs(matrix[i][maxValueColumn])

            return scalingFactors
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix_shape: {matrix.shape}")
            raise

    def getMaxValuePosition(self, matrix: np.ndarray) -> np.ndarray:
        try:
            if not isinstance(matrix, np.ndarray):
                raise ValueError("Error: Has ingresado una matriz inválida")

            maxValue = abs(matrix[0][0])
            maxValuePosition = np.array([0, 0], dtype=np.int8)

            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if matrix[i][j] > abs(maxValue):
                        maxValue = matrix[i][j]
                        maxValuePosition[0], maxValuePosition[1] = i, j

            return maxValuePosition
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"matrix_shape: {matrix.shape}")
            raise

    def sortResultByPosition(
        self, resultVector: np.ndarray, positionVector: np.ndarray
    ) -> np.ndarray:
        try:
            if len(resultVector) != len(positionVector):
                raise ValueError("Error: Los vectores deben tener la misma longitud")

            n = len(resultVector)
            orderedVector = np.zeros(n, dtype=np.float64)

            for i in range(n):
                currentResult = resultVector[i]
                targetPosition = positionVector[i]
                targetIndex = targetPosition - 1

                if 0 <= targetIndex < n:
                    orderedVector[targetIndex] = currentResult
            return orderedVector
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"resultVector_len: {len(resultVector)}, positionVector_len: {len(positionVector)}")
            raise

    def gaussSeidel(
        self, coefficients: np.ndarray, independents: np.ndarray, tol=1e-6, maxIter=1000
    ):
        try:
            n = len(independents)
            x = np.zeros(n)

            for _ in range(maxIter):
                xPrev = x.copy()
                for i in range(n):
                    sum1 = 0.0
                    for j in range(i):
                        sum1 += coefficients[i, j] * x[j]

                    sum2 = 0.0
                    for j in range(i + 1, n):
                        sum2 += coefficients[i, j] * xPrev[j]

                    x[i] = (independents[i] - sum1 - sum2) / coefficients[i, i]

                error = 0.0
                for i in range(n):
                    error += (x[i] - xPrev[i]) ** 2
                error = error**0.5

                if error < tol:
                    return x

            raise SystemDontHaveSolution(
                f"Gauss-Seidel no convergió después de {maxIter} iteraciones."
            )
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"coefficients_shape: {coefficients.shape}, independents_shape: {independents.shape}, tol: {tol}, maxIter: {maxIter}")
            raise