import numpy as np
from pathlib import Path
from datetime import datetime
import random
import time
from Apps.Common.Repositories.FileManager import FileManager

from errors import createLogFile

class FileWriter:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self):
        try:
            self.__resultsDir = Path("Storage/Results")
            self.__resultsDir.mkdir(parents=True, exist_ok=True)
        except Exception as error:
            createLogFile(self, error, error.__traceback__, "init")
            return None

    def __generateSerial(self) -> str:
        try:
            timestamp = int(time.time() % 1000000)
            random_num = random.randint(0, 0xFFFFFF)

            combined = (timestamp << 24) | random_num
            return f"{combined:08x}"
        except Exception as error:
            createLogFile(self, error, error.__traceback__, "__generateSerial")
            return None

    def __getCurrentDate(self) -> str:
        try:
            return datetime.now().strftime("%Y%m%d")
        except Exception as error:
            createLogFile(self, error, error.__traceback__, "__getCurrentDate")
            return None

    def __generateFileName(self, inputSerial: str) -> str:
        try:
            currentDate = self.__getCurrentDate()
            newSerial = self.__generateSerial()
            return f"{inputSerial}_{currentDate}_{newSerial}.txt"
        except Exception as error:
            createLogFile(self, error, error.__traceback__, inputSerial)
            return None

    def writeResultsToFile(self, dataArray: np.ndarray, inputSerial: str) -> str:
        try:
            if not isinstance(dataArray, np.ndarray) or dataArray.size == 0:
                raise ValueError("Los datos deben ser un array numpy no vacío")

            fileName = self.__generateFileName(inputSerial)
            filePath = self.__resultsDir / fileName

            with open(filePath, "w", encoding="utf-8") as file:
                file.write("Números escaneados:\n")
                for i in range(len(dataArray)):
                    for j in range(len(dataArray[i])):
                        if dataArray[i][j]:
                            file.write(str(dataArray[i][j]))
            return str(filePath)
        except Exception as error:
            createLogFile(self, error, error.__traceback__, inputSerial)
            return None

    def writeSystemOfEquationResult(self, dataArray: np.ndarray, inputSerial: str):
        try:
            if not isinstance(dataArray, np.ndarray) or dataArray.size == 0:
                raise ValueError("Los datos deben ser un array numpy no vacío")

            fileName = self.__generateFileName(inputSerial)
            filePath = self.__resultsDir / fileName

            with open(filePath, "w", encoding="utf-8") as file:
                file.write("Resultados del sistema de ecuaciones\n")
                for i in range(len(dataArray)):
                    file.write(f"x{i+1} = {dataArray[i]}\n")
            return str(filePath)
        except Exception as error:
            createLogFile(self, error, error.__traceback__, inputSerial)
            return None

    def writeEquationResults(
        self,
        equations: np.ndarray,
        variables: dict,
        results: np.ndarray,
        inputSerial: str,
    ):
        try:
            fileName = self.__generateFileName(inputSerial)
            filePath = self.__resultsDir / fileName

            with open(filePath, "w", encoding="utf-8") as file:
                file.write("Resultados de las ecuaciones\n\n")

                file.write("Variables utilizadas:\n\n")
                for name, value in variables.items():
                    file.write(f"{name} = {value}\n")
                file.write("\n\n")

                for i in range(len(equations)):
                    for j in range(len(equations[i])):
                        if equations[i][j]:
                            file.write(f"Ecuación: {equations[i][j]}\n")
                            file.write(f"Resultado = {results[i][j]}\n\n")
            return str(filePath)
        except Exception as error:
            createLogFile(self, error, error.__traceback__, inputSerial)
            return None

    def getFilePath(self, inputSerial: str) -> str:
        try:
            fileName = self.__generateFileName(inputSerial)
            filePath = self.__resultsDir / fileName
            return str(filePath)
        except Exception as error:
            createLogFile(self, error, error.__traceback__, inputSerial)
            return None

    def writeHeaderAndVariables(self, filePath: str, variables: dict):
        try:
            with open(filePath, "w", encoding="utf-8") as file:
                file.write("Resultados de las ecuaciones\n\n")

                file.write("Variables utilizadas:\n\n")
                for name, value in variables.items():
                    file.write(f"{name}\n")
                    file.write(f"{value}\n\n")
                file.write("\n\n")
        except Exception as error:
            createLogFile(self, error, error.__traceback__, filePath)
            return None

    def writeEquationAndResult(self, filePath: str, equation: str, result: np.ndarray):
        try:
            with open(filePath, "a", encoding="utf-8") as file:
                file.write(f"Ecuacion: {equation}\n")
                file.write("Resultado\n")
                file.write(f"{result}\n\n")
        except Exception as error:
            createLogFile(self, error, error.__traceback__, filePath)
            return None

    def writeEquationAndError(self, filePath: str, equation: str, errorMessage: str):
        try:
            with open(filePath, "a", encoding="utf-8") as file:
                file.write(f"Ecuacion: {equation}\n")
                file.write(errorMessage)
        except Exception as error:
            createLogFile(self, error, error.__traceback__, filePath)
            return None
