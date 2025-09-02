from Apps.NumericalMethods.Solvers.EquationSolvers.AbstractEquationSolver import AbstractEquationSolver
from Apps.NumericalMethods.Solvers.MatrixOperators.MatrixOperations import MatrixOperations
from Apps.NumericalMethods.Solvers.MatrixOperators.MatrixDimensionsOperations import MatrixDimensionsOperations

class DimensionsEquationSolver(AbstractEquationSolver):
    def __init__(self):
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

    def _evaluateOperator(self, operator, operand1, operand2):
        if operator not in self.operators:
            raise ValueError(f"Error: Operador desconocido: {operator}")
        return self.operators[operator](operand1, operand2)

    def _getOperatorPrecedence(self, operator):
        if operator not in self.precedences:
            raise ValueError(
                f"Error: Precedencia desconocida para el operador: {operator}"
            )
        return self.precedences[operator]

    def solve(self, equation: str, variables: dict = None) -> float:

        if variables is None:
            variables = {}
        vars = {}
        for key, value in variables.items():
            vars[key] = value.shape

        tokens = self._tokenize(equation)
        postfixNotation = self._shuntingYard(tokens)
        result = self._evaluatePostfix(postfixNotation, vars)
        return result
