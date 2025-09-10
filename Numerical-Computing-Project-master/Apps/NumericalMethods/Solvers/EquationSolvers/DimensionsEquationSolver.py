from Apps.NumericalMethods.Solvers.EquationSolvers.AbstractEquationSolver import AbstractEquationSolver
from Apps.NumericalMethods.Solvers.MatrixOperators.MatrixOperations import MatrixOperations
from Apps.NumericalMethods.Solvers.MatrixOperators.MatrixDimensionsOperations import MatrixDimensionsOperations
from Apps.Common.Repositories.FileManager import FileManager

class DimensionsEquationSolver(AbstractEquationSolver):
    """
    Solucionador de ecuaciones para operaciones con dimensiones de matrices.

    Hereda de AbstractEquationSolver e implementa la evaluación de operaciones de suma, resta y multiplicación de dimensiones de matrices.

    Métodos principales:
    - _evaluateOperator(operator, operand1, operand2): Evalúa la operación de dimensiones entre dos operandos usando el operador dado.

    Atributos:
    - matrixOperator: Instancia de MatrixDimensionsOperations para operar sobre dimensiones.
    - operators: Diccionario de operadores y sus funciones asociadas para dimensiones.
    - precedences: Diccionario de precedencias de operadores.
    """
    path = "Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    def __init__(self):
        try:
            self.matrixOperator = MatrixDimensionsOperations()
            super().__init__()
            self.operators = {
                "+": lambda x, y: self.matrixOperator.determineDimensionsOfAddition(x, y),
                "-": lambda x, y: self.matrixOperator.determineDimensionsOfSubstraction(
                    x, y
                ),
                "*": lambda x, y: self.matrixOperator.determineDimensionsOfMultiplication(
                    x, y
                ),
            }
            self.precedences = {
                "+": 1,
                "-": 1,
                "*": 2,
            }
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, "DimensionsEquationSolver.__init__")
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

    def solve(self, equation: str, variables: dict = None) -> float:
        try:
            if variables is None:
                variables = {}
            vars = {}
            for key, value in variables.items():
                vars[key] = value.shape

            tokens = self._tokenize(equation)
            postfixNotation = self._shuntingYard(tokens)
            result = self._evaluatePostfix(postfixNotation, vars)
            return result
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"equation: {equation}, variables: {variables}")
            raise