import os
import random

from Apps.Common.Helpers.ErrorHandling.ErrorLogger import ErrorLogger

class MatrixEquationGenerator:
    @staticmethod
    def generateComplexFormulas(fileName="MatrixFormulas.txt", outputPath=None, numFormulas=3):
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
        for _ in range(numFormulas):
            num_terms = random.randint(2, 4)
            formula_parts = []
            for i in range(num_terms):
                if random.random() < 0.3:
                    scalar = random.randint(2, 5)
                    matrix = random.choice(matrices)
                    formula_parts.append(f"{scalar} * {matrix}")
                else:
                    matrix = random.choice(matrices)
                    formula_parts.append(matrix)
                if i < num_terms - 1:
                    op = random.choice(operations)
                    formula_parts.append(op)
            formula = ' '.join(formula_parts)
            if formula not in formulas:
                formulas.append(formula)
            else:
                numFormulas += 1
        
        try:
            with open(fullPath, 'w') as file:
                for i, formula in enumerate(formulas[:numFormulas], 1):
                    file.write(f"{formula}\n")
            return fullPath
            
        except Exception as e:
            ErrorLogger.LogError(e, "Error al generar archivo de formulas")