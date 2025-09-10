import os
import numpy as np
from pathlib import Path
from Apps.Common.Helpers.ErrorHandling.Exceptions import *
from Apps.Common.Repositories.FileManager import FileManager
from errors import createLogFile  # Importa createLogFile

class FileReader:

    path = "Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self):
        self.__binaryFilesDir = Path("")

    def getFileList(self) -> np.ndarray:
        try:
            directories: np.ndarray = np.array(os.listdir(self.__binaryFilesDir))

            if len(directories) > 0:
                return directories
            else:
                raise FileNotFoundError("No se encontraron archivos.")

        except FileNotFoundError as error:
            createLogFile(self, error, error.__traceback__, str(self.__binaryFilesDir))
            raise FileNotFoundError(
                f"Error: No se ha encontrado archivos en el directorio {self.__binaryFilesDir}"
            )

        except NotADirectoryError as error:
            createLogFile(self, error, error.__traceback__, str(self.__binaryFilesDir))
            raise NotADirectoryError(
                f"Error: {self.__binaryFilesDir} no es un directorio"
            )

    def getRowCount(self, fileName: str) -> int:
        filePath = self.__binaryFilesDir / fileName
        if not filePath.exists():
            raise FileNotFoundError(f"Archivo {fileName} no encontrado")

        with open(filePath, "rb") as file:
            return len(file.readlines())

    def getColumnCount(self, fileName: str) -> int:
        filePath = self.__binaryFilesDir / fileName
        if not filePath.exists():
            raise FileNotFoundError(f"Archivo {fileName} no encontrado")

        maxColumns: int = 0

        with open(filePath, "rb") as file:
            for line in file:
                cleanLine = line.decode("utf-8")
                if not cleanLine:
                    continue

                columns: list = cleanLine.split("#")
                currentColumns = len(columns)

                if currentColumns > maxColumns:
                    maxColumns = currentColumns

            return maxColumns

    def readBinaryFile(self, fileName: str) -> np.ndarray:
        filePath = self.__binaryFilesDir / fileName
        if not filePath.exists():
            raise FileNotFoundError(f"Archivo {fileName} no encontrado")

        rows = self.getRowCount(fileName)
        cols = self.getColumnCount(fileName)

        result_array = np.empty((rows, cols), dtype="object")

        with open(filePath, "rb") as file:
            i = 0
            line = file.readline().decode("utf-8")
            while line:
                content = line.split("#")

                for j in range(len(content)):
                    if len(content[j]) == 0:
                        continue
                    result_array[i][j] = content[j].strip()

                i += 1
                line = file.readline().decode("utf-8")

        return result_array
