from Apps.NumericalMethods.Solvers.EquationSolvers.AbstractEquationSolver import AbstractEquationSolver
from Apps.NumericalMethods.Solvers.MatrixOperators.MatrixOperations import MatrixOperations
from Apps.Common.Repositories.FileManager import FileManager

class MatrixEquationSolver(AbstractEquationSolver):
    path = "Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    def __init__(self):
        try:
            self.matrixOperator = MatrixOperations()
            super().__init__()
            self.operators = {
                "+": lambda x, y: self.matrixOperator.add(x, y),
                "-": lambda x, y: self.matrixOperator.subtract(x, y),
                "*": lambda x, y: self.matrixOperator.multiply(x, y),
            }
            self.precedences = {
                "+": 1,
                "-": 1,
                "*": 2,
            }
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, "MatrixEquationSolver.__init__")
            raise

    def _evaluateOperator(self, operator, operand1, operand2):
        try:
            if operator not in self.operators:
                raise ValueError(f"Error: Operador desconocido: {operator}")
            return self.operators[operator](operand1, operand2)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"operator: {operator}, operand1_shape: {operand1.shape if hasattr(operand1, 'shape') else 'N/A'}, operand2_shape: {operand2.shape if hasattr(operand2, 'shape') else 'N/A'}")
            raise

    def _getOperatorPrecedence(self, operator):
        try:
            if operator not in self.precedences:
                raise ValueError(
                    f"Error: Precedencia desconocida para el operador: {operator}"
                )
            return self.precedences[operator]
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"operator: {operator}")
            raise