from Apps.NumericalMethods.Solvers.EquationSolvers.AbstractEquationSolver import AbstractEquationSolver
from Apps.Common.Repositories.FileManager import FileManager

class BasicEquationSolver(AbstractEquationSolver):
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    def __init__(self):
        try:
            super().__init__()
            self.operators = {
                "+": lambda x, y: x + y,
                "-": lambda x, y: x - y,
                "*": lambda x, y: x * y,
                "/": lambda x, y: x / y,
                "^": lambda x, y: x**y,
            }
            self.precedences = {"+": 1, "-": 1, "*": 2, "/": 2, "**": 3}
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, "BasicEquationSolver.__init__")
            raise

    def _evaluateOperator(self, operator, operand1, operand2):
        try:
            if operator not in self.operators:
                raise ValueError(f"Error: Operador desconocido: {operator}")
            return self.operators[operator](operand1, operand2)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"operator: {operator}, operand1: {operand1}, operand2: {operand2}")
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