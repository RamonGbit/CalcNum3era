import os
import random

class archiveGenerator():
    __router = ""
    __nameArchive = ""

    def __init__(self, nameArchive = "generalArchive.bin", router = None):#constructor polimorfico
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

    def setRouter(self, router):
        """
        Cambio de ruta existente

        ->@param: string router = C:\\folder1\\folder2\\folder or "C:\folder\folder\folder" or C:/folder/folder/folder
        ->@return: Void
        """
        if (not router or len(router) == 0):
            raise Exception("Manage-Error: La ruta es vacia.")
        self.utilDirectory(router)

    def setName(self, nameArchive):
        """
        Cambio de ruta existente

        ->@param: string [archive.extension]
        ->@return: Void
        """
        if (not nameArchive or len(nameArchive) == 0):
            raise Exception("Manage-Error: La ruta es vacia.")
        print(nameArchive)
        self.__nameArchive = nameArchive

    def __setOrCreateFiles(self, nameArchive, content = "", overwrite = False):
        if (not nameArchive or len(nameArchive) == 0):
            raise Exception("Manage-Error: El nombre esta Vacio.")
        try:
            filePath = self.__router + "\\" + nameArchive
            mode = 'w' if overwrite else 'a'
            with open(filePath, mode) as archive:
                if content:
                    archive.write(content)
        except FileNotFoundError as e:
            print("Manage-Error: El archivo no ha sido encontrado", e)

    def archiveDataGenerator(self, row = 3, colum = 4):
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

    def __utilDirectory(self, router):
        
        if (os.path.exists(router) and not os.path.isdir(router)):
            raise NotADirectoryError(f"Manage-Error: La ruta '{router}' no es un directorio.")
        elif (not os.path.exists(router)):
            raise FileNotFoundError(f"Manage-Error: El directorio '{router}' no existe.")
        
        self.__router = router
