from Apps.Common.Repositories.FileManager import FileManager

def contador(path):
    path = "Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            return len(lines) if  len(lines) else 0
    except Exception as error:
        from errors import createLogFile
        createLogFile(fileManager   , error, error.__traceback__, "SystemOfEquationsSolver.__init__")