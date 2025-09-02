class SystemDontHaveSolution(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NumberIsInvalid(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NoneType(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ImposibleMatrixOperation(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidOperators(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidBrackets(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidEquation(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class VariableNotExist(Exception):
    def __init__(self, message: str):
        super().__init__(message)
