from Apps.Common.Repositories.FileManager import FileManager

class RelativeError:
    __value: float = 0.0
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, exactValue: float, aproximatedValue: float):
        try:
            if not isinstance(exactValue, float) and not isinstance(
                aproximatedValue, float
            ):
                raise ValueError("Error: Solo se aceptan valores float")

            self._calculateAndSetRelativeError(exactValue, aproximatedValue)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"exactValue={exactValue}, aproximatedValue={aproximatedValue}")
            return None

    def _calculateAndSetRelativeError(
        self, exactValue: float, aproximatedValue: float
    ) -> None:
        try:
            self.__value = (exactValue - aproximatedValue) / exactValue
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"exactValue={exactValue}, aproximatedValue={aproximatedValue}")
            return None

    def getValue(self) -> float:
        try:
            return self.__value
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"value={self.__value}")
            return None

    def __str__(self) -> str:
        try:
            return f"Error Relativo: {self.__value * 100}%"
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"value={self.__value}")
            return None
