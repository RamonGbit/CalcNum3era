import os
import numpy as np
from .arrays import appendArray
from typing import TextIO
from array import ArrayType


class FileManager:
    """Un manejador de archivos y directorios para listar, leer y escribir archivos.

    Attributes:
        path (str): Ruta del directorio.
    """
    __path = os.getcwd()

    def __init__(self, path: str = os.getcwd()):
        print(path)
        if len(path) == 0:
            raise Exception("Manage-Error: Debe ingresar una ruta")
        self.__path = self.__utilPath(path)

    def setRouter(self, path: str) -> None:
        """Establece la ruta del directorio.

        Args:
            path (str): Ruta del directorio.
        """
        if len(path) == 0:
            raise Exception("Manage-Error: Debe ingresar una ruta")
        self.__path = self.__utilPath(path)

    def openFile(self, fileName: str) -> TextIO:
        """Abre un archivo con la function open.

        Args:
            fileName (str): Nombre del archivo.

        Returns:
            TextIO: Contenido del archivo.
        """
        filePath = os.path.join(self.__path, fileName)
        try:
            file = open(filePath, "rb")
            return file
        except FileNotFoundError as error:
            from errors import createLogFile
            createLogFile(self, error, error.__traceback__, filePath)
            return None

    def listFiles(self) -> ArrayType[str]:
        """Devuelve una lista de los archivos en el directorio.

        Returns:
            ArrayType[str]: Lista de los archivos en el directorio.
        """
        directoryEntries = np.array(os.listdir(self.__path))
        files = np.array([])
        for entry in directoryEntries:
            if entry.endswith(".bin"):
                files = appendArray(files, str(entry))
        return files

    def getPath(self) -> str:
        """Devuelve la ruta del directorio.

        Returns:
            str: Ruta del directorio.
        """
        return self.__path

    def writeFile(self, fileName: str, content: str) -> None:
        """Escribe contenido en un archivo.

        Args:
            fileName (str): Nombre del archivo.
            content (str): Contenido del archivo.
        """
        filePath = os.path.join(self.__path, fileName)
        try:
            file = open(filePath, "a")
            file.write(content)
        except FileNotFoundError as error:
            from errors import createLogFile
            createLogFile(self, error, error.__traceback__, filePath)

    def __utilPath(self, path: str) -> str:
        """Valida la ruta ingresada.

        Args:
            path (str): Ruta a validar.

        Returns:
            str: Ruta absoluta.
        """
        if not os.path.exists(path):
            raise Exception("Manage-Error: La ruta ingresada no existe")
        if not os.path.isdir(path):
            raise Exception(
                "Manage-Error: La ruta ingresada no es un directorio")
        return path
