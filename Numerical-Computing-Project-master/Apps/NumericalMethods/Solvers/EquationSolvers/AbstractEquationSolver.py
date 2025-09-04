from abc import ABC, abstractmethod
from Apps.Common.Helpers.ErrorHandling.Exceptions import *
from Apps.Common.Structures.LinkedList import LinkedList
from Apps.Common.Structures.queue import Queue  # Cambiado a 'queue' minúscula
from Apps.Common.Structures.stack import Stack  # Cambiado a 'stack' minúscula
import numpy as np


class AbstractEquationSolver(ABC):
    def __init__(self):
        self.operators = {}
        self.precedences = {}
        self.brackets = {"(": ")", "[": "]", "{": "}"}
        self.openBrackets = set(self.brackets.keys())
        self.closeBrackets = set(self.brackets.values())
        self.variableChars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

    @abstractmethod
    def _evaluateOperator(self, operator, operand1, operand2):
        pass

    @abstractmethod
    def _getOperatorPrecedence(self, operator: str) -> int:
        pass

    def _isOperator(self, token) -> bool:
        return token in self.operators

    def _isNumber(self, token: str) -> bool:
        numbers = "0123456789."
        for i in range(len(token)):
            if not token[i] in numbers:
                return False
        return True

    def _isVariable(self, token):
        return len(token) == 1 and token in self.variableChars

    def _tokenize(self, expression: str) -> LinkedList:
        tokens = LinkedList()
        i = 0
        while i < len(expression):
            char = expression[i]

            if char == " ":
                i += 1
                continue

            elif (
                self._isOperator(char)
                or char in self.openBrackets
                or char in self.closeBrackets
            ):
                if (
                    char in self.openBrackets
                    and tokens.getSize() != 0
                    and (
                        self._isNumber(tokens.get(-1))
                        or self._isVariable(tokens.get(-1))
                    )
                ):
                    tokens.addLast("*")
                tokens.addLast(char)
                i += 1

            elif self._isNumber(char) or (
                char == "."
                and i + 1 < len(expression)
                and self._isNumber(expression[i + 1])
            ):
                num_str = ""
                while i < len(expression) and (
                    self._isNumber(expression[i]) or expression[i] == "."
                ):
                    num_str += expression[i]
                    i += 1
                tokens.addLast(num_str)

                if i < len(expression) and expression[i] in self.variableChars:
                    tokens.addLast("*")

            elif char in self.variableChars:
                if tokens.getSize() != 0 and (
                    self._isNumber(tokens.get(-1)) or self._isVariable(tokens.get(-1))
                ):
                    tokens.addLast("*")

                tokens.addLast(char)
                i += 1

                if i < len(expression) and expression[i] in self.openBrackets:
                    tokens.addLast("*")
            else:
                raise InvalidOperators(
                    f"Caracter desconocido o inesperado en la expresión: '{char}' en la posición {i}"
                )
        return tokens

    def _shuntingYard(self, tokens: LinkedList) -> Queue:
        outputQueue = Queue()
        operatorStack = Stack()

        for i in range(tokens.getSize()):
            token: str = tokens.get(i)

            if self._isNumber(token):
                outputQueue.enqueue(float(token))

            elif self._isVariable(token):
                outputQueue.enqueue(token)

            elif token in self.openBrackets:
                operatorStack.push(token)

            elif token in self.closeBrackets:
                openedBracket = None
                for openBracker, closeBracked in self.brackets.items():
                    if closeBracked == token:
                        openedBracket = openBracker
                        break

                if not openedBracket:
                    raise InvalidBrackets(
                        f"Paréntesis de cierre no reconocido: {token}"
                    )

                while (
                    operatorStack.getSize() > 0
                    and operatorStack.showStack() != openedBracket
                ):
                    outputQueue.enqueue(operatorStack.pop())

                if (
                    operatorStack.getSize() == 0
                    or operatorStack.showStack() != openedBracket
                ):
                    raise InvalidBrackets(
                        "Paréntesis, corchetes o llaves no balanceados."
                    )

                operatorStack.pop()

            elif self._isOperator(token):

                while (
                    operatorStack.getSize() > 0
                    and operatorStack.showStack() in self.operators
                    and self._getOperatorPrecedence(operatorStack.showStack())
                    >= self._getOperatorPrecedence(token)
                ):

                    outputQueue.enqueue(operatorStack.pop())
                operatorStack.push(token)

            else:
                raise InvalidOperators(f"Error: Token no reconocido: {token}")

        while operatorStack.getSize() > 0:
            if operatorStack.showStack() in self.openBrackets:
                raise ValueError("Paréntesis, corchetes o llaves no balanceados.")
            outputQueue.enqueue(operatorStack.pop())

        return outputQueue

    def _evaluatePostfix(self, postfixNotation: Queue, variables: dict) -> float:
        if not isinstance(postfixNotation, Queue) or not isinstance(variables, dict):
            raise ValueError(
                "Error: Has ingresado una pila inválida o un diccionario inválido"
            )

        operandStack = Stack()

        for i in range(postfixNotation.getSize()):
            token = postfixNotation.dequeue()

            if isinstance(token, (int, float)):
                operandStack.push(token)

            elif self._isVariable(token):
                if token not in variables:
                    raise VariableNotExist(
                        f"Error: Variable '{token}' no definida en el diccionario."
                    )
                operandStack.push(variables[token])

            elif self._isOperator(token):
                if operandStack.getSize() < 2:
                    raise InvalidEquation(
                        "Error: Expresión postfija inválida: pocos operandos para el operador "
                        + token
                    )

                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                result = self._evaluateOperator(token, operand1, operand2)
                operandStack.push(result)

        if operandStack.getSize() != 1:
            raise InvalidEquation(
                "Error: Expresión postfija inválida. Demasiados operandos o operadores."
            )

        return operandStack.pop()

    def solve(self, equation: str, variables: dict = None) -> float:

        if variables is None:
            variables = {}

        tokens = self._tokenize(equation)
        postfixNotation = self._shuntingYard(tokens)
        result = self._evaluatePostfix(postfixNotation, variables)
        return result
