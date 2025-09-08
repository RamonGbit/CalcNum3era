import os
import numpy as np
from typing import TextIO
from Apps.Common.Helpers.ErrorHandling.ErrorLogger import ErrorLogger
from .arrays import appendArray


class FileManager:
    __path = os.getcwd()

    def __init__(self, path: str = os.getcwd()):
        if len(path) == 0:
            raise Exception("Manage-Error: Debe ingresar una ruta")
        self.__path = self.__utilPath(path)

    def setRouter(self, path: str) -> None:
        if len(path) == 0:
            raise Exception("Manage-Error: Debe ingresar una ruta")
        self.__path = self.__utilPath(path)

    def openFile(self, fileName: str) -> TextIO:
        filePath = os.path.join(self.__path, fileName)
        try:
            file = open(filePath, "r", encoding="utf-8")
            return file
        except FileNotFoundError as error:
            ErrorLogger.LogError(error, f"Archivo no encontrado en {filePath}")
            return None

    def listFiles(self) -> np.ndarray:
        directoryEntries = np.array(os.listdir(self.__path))
        files = np.array([])
        for entry in directoryEntries:
            if entry.endswith(".bin"):
                files = appendArray(files, str(entry))
        return files

    def getPath(self) -> str:
        return self.__path

    def writeFile(self, fileName: str, content: str) -> None:
        filePath = os.path.join(self.__path, fileName)
        try:
            file = open(filePath, "a", encoding="utf-8")
            file.write(content)
        except FileNotFoundError as error:
            ErrorLogger.LogError(error, f"Error de archivo en {filePath}")

    def __utilPath(self, path: str) -> str:
        if not os.path.exists(path):
            raise Exception("Manage-Error: La ruta ingresada no existe")
        if not os.path.isdir(path):
            raise Exception(
                "Manage-Error: La ruta ingresada no es un directorio")
        return path