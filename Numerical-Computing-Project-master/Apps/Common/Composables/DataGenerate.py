import os
import random
from Apps.Common.Repositories.FileManager import FileManager

class archiveGenerator():
    __router = ""
    __nameArchive = ""
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, nameArchive = "generalArchive.bin", router = None):#constructor polimorfico
        try:
            # Usar Storage/Data en la raíz por defecto
            if router is None:
                router = os.path.join(os.getcwd(), "Storage", "Data")
                os.makedirs(router, exist_ok=True)
            """
            Crear o modificar archivos. 
            
            ->@param: string [archive.extension]
            ->@param: string router = C:\\folder1\\folder2\\folder or "C:\folder\folder\folder" or C:/folder/folder/folder
            ->@return: Void
            """
            if (not router or len(router) == 0):
                raise Exception("Manage-Error: La ruta es vacia.")
            
            if (len(nameArchive) == 0 or not nameArchive):
                raise Exception("Manage-Error: La ruta es vacia.")
            
            self.__nameArchive = nameArchive
            self.__utilDirectory(router)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self, error, error.__traceback__, nameArchive)
            return None

    def setRouter(self, router):
        try:
            """
            Cambio de ruta existente

            ->@param: string router = C:\\folder1\\folder2\\folder or "C:\folder\folder\folder" or C:/folder/folder/folder
            ->@return: Void
            """
            if (not router or len(router) == 0):
                raise Exception("Manage-Error: La ruta es vacia.")
            self.utilDirectory(router)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self, error, error.__traceback__, router)
            return None

    def setName(self, nameArchive):
        try:
            """
            Cambio de ruta existente

            ->@param: string [archive.extension]
            ->@return: Void
            """
            if (not nameArchive or len(nameArchive) == 0):
                raise Exception("Manage-Error: La ruta es vacia.")
            print(nameArchive)
            self.__nameArchive = nameArchive
        except Exception as error:
            from errors import createLogFile
            createLogFile(self, error, error.__traceback__, nameArchive)
            return None

    def __setOrCreateFiles(self, nameArchive, content = "", overwrite = False):
        try:
            if (not nameArchive or len(nameArchive) == 0):
                raise Exception("Manage-Error: El nombre esta Vacio.")
            filePath = self.__router + "\\" + nameArchive
            mode = 'w' if overwrite else 'a'
            with open(filePath, mode) as archive:
                if content:
                    archive.write(content)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self, error, error.__traceback__, nameArchive)
            return None

    def archiveDataGenerator(self, row = 3, colum = 4):
        try:
            """
            Genera archivo con datos aleatorios.

            ->@param: Float/Float [data default = 3]
            ->@return: Void
            """
            arrayBi = []

            if row > 0 and colum > 0:
                arrayBi = [[random.randint(-30, 30) for j in range(colum)] for i in range(row)]

                # Construir el contenido completo como string
                lines = []
                for i in range(len(arrayBi)):
                    line = '/'.join(str(x) for x in arrayBi[i])
                    lines.append(line)
                content = '\n'.join(lines) + '\n'
                # Sobrescribir el archivo con todo el contenido
                self.__setOrCreateFiles(self.__nameArchive, content, overwrite=True)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self, error, error.__traceback__, f"row={row}, colum={colum}")
            return None

    def __utilDirectory(self, router):
        try:
            if (os.path.exists(router) and not os.path.isdir(router)):
                raise NotADirectoryError(f"Manage-Error: La ruta '{router}' no es un directorio.")
            elif (not os.path.exists(router)):
                raise FileNotFoundError(f"Manage-Error: El directorio '{router}' no existe.")
            
            self.__router = router
        except Exception as error:
            from errors import createLogFile
            createLogFile(self, error, error.__traceback__, router)
            return None
