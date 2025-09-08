import os
import random
from errors import createLogFile
from Apps.Common.Repositories.FileManager import FileManager

class MatrixEquationGenerator:

    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    @staticmethod
    def generateComplexFormulas(fileName="MatrixFormulas.txt", outputPath=None, numFormulas=3):
        try:
            # Usar Storage/Data en la raíz por defecto
            if outputPath is None:
                outputPath = os.path.join(os.getcwd(), "Storage", "Data")
                os.makedirs(outputPath, exist_ok=True)
            fullPath = os.path.join(outputPath, fileName)
            if not os.path.exists(outputPath):
                raise FileNotFoundError(f"El directorio {outputPath} no existe")
            
            matrices = ['A', 'B', 'C']
            operations = ['+', '-']         
            formulas = []
            i = 0
            while i < numFormulas:
                num_terms = random.randint(2, 4)
                formula_parts = []
                for j in range(num_terms):
                    if random.random() < 0.3:
                        scalar = random.randint(2, 5)
                        matrix = random.choice(matrices)
                        formula_parts.append(f"{scalar} * {matrix}")
                    else:
                        matrix = random.choice(matrices)
                        formula_parts.append(matrix)
                    if j < num_terms - 1:
                        op = random.choice(operations)
                        formula_parts.append(op)
                formula = ' '.join(formula_parts)
                if formula not in formulas:
                    formulas.append(formula)
                    i += 1
                else:
                    # Si la fórmula ya existe, no incrementamos i para generar otra
                    pass
            
            with open(fullPath, 'w') as file:
                for formula in formulas:
                    file.write(f"{formula}\n")
            return fullPath

        except Exception as error:
            createLogFile(MatrixEquationGenerator, error, error.__traceback__, fileName)
            return None
