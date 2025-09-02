from Repositories.CalculatedErrors.AbsoluteError import AbsoluteError
from Repositories.CalculatedErrors.RelativeError import RelativeError


class RoundingError(AbsoluteError, RelativeError):
    __absoluteError: float = 0.0
    __relativeError: float = 0.0

    def __init__(self, exactValue: float, aproximatedValue: float):
        if not isinstance(exactValue, float) and not isinstance(
            aproximatedValue, float
        ):
            raise ValueError("Error: Solo se aceptan valores float")

        self._calculateAndSetAbsoluteError(exactValue, aproximatedValue)
        self._calculateAndSetRelativeError(exactValue, aproximatedValue)

    def __str__(self) -> str:
        return f"""
Error por redondeo: {self.__absoluteError} unidades
El error representa un {self.__relativeError * 100}% del valor exacto
    """
