from Apps.NumericalMethods.Solvers.EquationSolvers.AbstractEquationSolver import AbstractEquationSolver
from Apps.NumericalMethods.Solvers.MatrixOperators.MatrixOperations import MatrixOperations


class MatrixEquationSolver(AbstractEquationSolver):
    def __init__(self):
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
