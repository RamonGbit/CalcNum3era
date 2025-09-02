import numpy as np
from pathlib import Path
from datetime import datetime
import random
import time


class FileWriter:

    def __init__(self):
        self.__resultsDir = Path("Storage/Results")
        self.__resultsDir.mkdir(parents=True, exist_ok=True)

    def __generateSerial(self) -> str:
        timestamp = int(time.time() % 1000000)
        random_num = random.randint(0, 0xFFFFFF)

        combined = (timestamp << 24) | random_num
        return f"{combined:08x}"

    def __getCurrentDate(self) -> str:
        return datetime.now().strftime("%Y%m%d")

    def __generateFileName(self, inputSerial: str) -> str:
        currentDate = self.__getCurrentDate()
        newSerial = self.__generateSerial()
        return f"{inputSerial}_{currentDate}_{newSerial}.txt"

    def writeResultsToFile(self, dataArray: np.ndarray, inputSerial: str) -> str:
        if not isinstance(dataArray, np.ndarray) or dataArray.size == 0:
            raise ValueError("Los datos deben ser un array numpy no vacío")

        fileName = self.__generateFileName(inputSerial)
        filePath = self.__resultsDir / fileName

        with open(filePath, "w", encoding="utf-8") as file:
            file.write("Números escaneados:")
            file.write("\n")
            for i in range(len(dataArray)):
                for j in range(len(dataArray[i])):
                    if dataArray[i][j]:
                        file.write(dataArray[i][j].__str__())

    def writeSystemOfEquationResult(self, dataArray: np.ndarray, inputSerial: str):
        if not isinstance(dataArray, np.ndarray) or dataArray.size == 0:
            raise ValueError("Los datos deben ser un array numpy no vacío")

        fileName = self.__generateFileName(inputSerial)
        filePath = self.__resultsDir / fileName

        with open(filePath, "w", encoding="utf-8") as file:
            file.write("Resultados del sistema de ecuaciones")
            file.write("\n")
            for i in range(len(dataArray)):
                file.write(f"x{i+1} = {dataArray[i]}\n")

    def writeEquationResults(
        self,
        equations: np.ndarray,
        variables: dict,
        results: np.ndarray,
        inputSerial: str,
    ):
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

    def getFilePath(self, inputSerial: str) -> str:
        fileName = self.__generateFileName(inputSerial)
        filePath = self.__resultsDir / fileName
        return filePath

    def writeHeaderAndVariables(self, filePath: str, variables: dict):
        with open(filePath, "w", encoding="utf-8") as file:
            file.write("Resultados de las ecuaciones\n\n")

            file.write("Variables utilizadas:\n\n")
            for name, value in variables.items():
                file.write(f"{name}\n")
                file.write(f"{value}")
                file.write("\n\n")
            file.write("\n\n")

    def writeEquationAndResult(self, filePath: str, equation: str, result: np.ndarray):
        with open(filePath, "a", encoding="utf-8") as file:
            file.write(f"Ecuacion: {equation}\n")
            file.write("Resultado\n")
            file.write(f"{result}\n\n")

    def writeEquationAndError(self, filePath: str, equation: str, errorMessage: str):
        with open(filePath, "a", encoding="utf-8") as file:
            file.write(f"Ecuacion: {equation}\n")
            file.write(errorMessage)
