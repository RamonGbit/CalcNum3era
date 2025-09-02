import sys
import traceback
from datetime import datetime


class ErrorLogger:
    _logFile = "errors.log"
    _executionSerial = 0

    @staticmethod
    def LogError(exception: Exception, errorType: str = "Excepción expulsada"):
        ErrorLogger._executionSerial += 1
        currentDate = datetime.now().strftime("%Y%m%d_%H%M%S")

        excType, excValue, excTraceback = sys.exc_info()

        fileName = "ArchivoDesconocido"
        lineNumber = "LineaDesconocida"
        if excTraceback:
            tb = excTraceback
            while tb.tb_next:
                tb = tb.tb_next
            fileName = tb.tb_frame.f_code.co_filename
            lineNumber = tb.tb_frame.f_lineno

        errorName = type(exception).__name__
        formattedErrorMessage = (
            f"{errorName}_{currentDate}_{ErrorLogger._executionSerial}: "
            f"Error [{errorType}/ {str(exception)}/ {fileName}:{lineNumber}]\n"
        )

        with open(ErrorLogger._logFile, "a", encoding="utf-8") as logFile:
            logFile.write(formattedErrorMessage)
