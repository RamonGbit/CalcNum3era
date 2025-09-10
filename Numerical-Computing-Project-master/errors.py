from datetime import datetime
from random import randint
import traceback
from typing import Any
from Apps.Common.Repositories.FileManager import FileManager


def createLogFile(manager   : FileManager, error: Exception, trace: any, value: Any) -> None:
    tb = traceback.extract_tb(trace)
    oldPath = manager.getPath()
    manager.setRouter(".")
    now = datetime.now().strftime("%d/%m/%Y")
    serial = randint(1000, 9999)
    errorName = error.__class__.__name__
    ubication = f"{tb[0].filename}: linea {tb[0].lineno} / {tb[0].name}"
    print("HA OCURRIDO UN ERROR")
    errorLog = f"{errorName}_{now}_{serial}: [{error} / {value} / {ubication}]\n"
    manager.writeFile("errors.log", errorLog)
    manager.setRouter(oldPath)
