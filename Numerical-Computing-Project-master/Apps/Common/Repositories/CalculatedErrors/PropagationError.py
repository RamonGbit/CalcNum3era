from Repositories.CalculatedErrors.AbsoluteError import AbsoluteError
from Repositories.CalculatedErrors.RelativeError import RelativeError
from Apps.Common.Repositories.FileManager import FileManager

class PropagationError(AbsoluteError, RelativeError):

    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    __absoluteError: float = 0.0
    __relativeError: float = 0.0

    def __init__(self, exactValue: float, aproximatedValue: float):
        try:
            if not isinstance(exactValue, float) and not isinstance(
                aproximatedValue, float
            ):
                raise ValueError("Error: Solo se aceptan valores float")

            self._calculateAndSetAbsoluteError(exactValue, aproximatedValue)
            self._calculateAndSetRelativeError(exactValue, aproximatedValue)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"exactValue={exactValue}, aproximatedValue={aproximatedValue}")
            return None

    def __str__(self) -> str:
        try:
            return f"""
Error por propagación: {self.__absoluteError} unidades
El error representa un {self.__relativeError * 100}% del valor exacto
    """
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"absoluteError={self.__absoluteError}, relativeError={self.__relativeError}")
            return None