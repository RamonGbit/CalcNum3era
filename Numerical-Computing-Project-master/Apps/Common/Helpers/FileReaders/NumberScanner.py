from Apps.Common.Helpers.FileReaders.FileReader import FileReader
from Apps.Common.Helpers.ErrorHandling.Exceptions import *
from Apps.Common.Helpers.ErrorHandling.ErrorLogger import ErrorLogger
from Apps.Common.Repositories.StudiedNumbers.StudiedNumber import StudiedNumber
from Apps.Common.Composables.FileWriter import FileWriter
import numpy as np

class NumberScanner:
    def scanAnalizeAndWriteResults(self, fileName:str) -> None:
        fileWriter = FileWriter()
        readedFileSerial = fileName.split("_")[2].split(".")[0]
        scannedValues = self.readMatrixFile(fileName)

        numbers = np.empty((len(scannedValues), len(scannedValues[0])), dtype="object")

        self.__fillNumbersArray(numbers, scannedValues)
        fileWriter.writeResultsToFile(numbers, readedFileSerial)

    def readMatrixFile(self, fileName: str) -> list[list[str]]:
        import os
        data_dir = os.path.join(os.getcwd(), "Storage", "Data")
        file_path = os.path.join(data_dir, fileName)
        result = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                columns = line.split("/")
                result.append([col.strip() for col in columns if col.strip() != ""])
        return result

    def __fillNumbersArray(
        self, numbers: np.ndarray, scannedValues: np.ndarray) -> None:
        for i in range(len(scannedValues)):
            for j in range(len(scannedValues[i])):
                try:
                    if scannedValues[i][j]:
                        numbers[i][j] = StudiedNumber(scannedValues[i][j].strip())
                except NumberIsInvalid:
                    numbers[i][j] = f"\n{scannedValues[i][j]}: Es un valor inválido\n"
                except NoneType:
                    continue
                except (ValueError, TypeError) as error:
                    ErrorLogger.LogError(error)
