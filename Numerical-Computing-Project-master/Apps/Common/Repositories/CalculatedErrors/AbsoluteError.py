class AbsoluteError:
    __value: float = 0.0

    def __init__(self, exactValue: float, aproximatedValue: float):
        if not isinstance(exactValue, float) and not isinstance(
            aproximatedValue, float
        ):
            raise ValueError("Error: Solo se aceptan valores float")

        self._calculateAndSetAbsoluteError(exactValue, aproximatedValue)

    def _calculateAndSetAbsoluteError(
        self, exactValue: float, aproximatedValue: float
    ) -> None:
        self.__value = exactValue - aproximatedValue

    def getValue(self) -> float:
        return self.__value

    def __str__(self) -> str:
        return f"Error Absoluto: {self.__value} unidades"
