import numpy as np
from fractions import Fraction
import datetime
from errors import createLogFile
from Apps.Common.Repositories.FileManager import FileManager

class MathReport:

    path = "Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, reportFile="mathReport"):
        import os
        import uuid
        from datetime import datetime
        try:
            results_dir = os.path.join(os.getcwd(), "Storage", "Results")
            os.makedirs(results_dir, exist_ok=True)
            fecha_actual = datetime.now().strftime("%Y%m%d")
            serial = uuid.uuid4().hex[:8]
            nombre_archivo = f"{reportFile}_{fecha_actual}_{serial}.txt"
            self.reportFile = os.path.join(results_dir, nombre_archivo)
            self._initializeReport()
        except Exception as error:
            createLogFile(self.fileManager, error, error.__traceback__, reportFile)
            return None

    def _initializeReport(self):
        try:
            with open(self.reportFile, "w") as file:
                file.write("--- REPORTE DE OPERACIONES MATRICIALES Y SISTEMAS ---\n")
                file.write(f"Fecha: {datetime.date.today()}\n")
        except Exception as error:
            createLogFile(self.fileManager, error, error.__traceback__, error)
            return None

    def _formatMatrixToString(self, matrix, name="", addBraces=False, addPipe=False):
        try:
            lines = []
            if addBraces:
                lines.append("{")
            for rowIdx, row in enumerate(matrix):
                formattedRow = []
                for colIdx, value in enumerate(row):
                    if value == int(value):
                        formattedRow.append(f"{int(value):>7}")
                    else:
                        try:
                            fraction = Fraction(value).limit_denominator(1000)
                            if fraction.denominator == 1:
                                formattedRow.append(f"{fraction.numerator:>7}")
                            else:
                                formattedRow.append(f"{str(fraction):>7}")
                        except OverflowError:
                            formattedRow.append(f"{value:>7.3f}")
                rowStr = "  ".join(formattedRow)
                if addPipe and matrix.shape[1] == 4 and colIdx == matrix.shape[1] - 1:
                    rowStr = rowStr[:-(len(formattedRow[-1]) + 2)] + " | " + formattedRow[-1]
                lines.append(f"  [ {rowStr} ]")
            if addBraces:
                lines.append("}")
            return "\n".join(lines)
        except Exception as error:
            createLogFile(self.fileManager, error, error.__traceback__, "matrix_formatting")
            return None

    def writeOriginalMatrices(self, matrices: dict):
        try:
            with open(self.reportFile, "a") as file:
                file.write("--- MATRICES ORIGINALES ---\n\n")
                for name, matrix in matrices.items():
                    file.write(f"Matriz {name} ({matrix.shape[0]}x{matrix.shape[1]}):\n")
                    file.write(self._formatMatrixToString(matrix, addPipe=True) + "\n\n")
                file.write("\n")
        except Exception as error:
            createLogFile(self.fileManager, error, error.__traceback__, self.reportFile)
            return None

    def writeFormulasAndResults(self, formulas: list[str], results: list[np.ndarray]):
        try:
            if len(formulas) != len(results):
                raise ValueError("La lista de formulas y resultados debe tener el mismo tamaño.")
            with open(self.reportFile, "a") as file:
                file.write("--- RESOLUCION DE FORMULAS CON MATRICES ---\n\n")
                for i, formula in enumerate(formulas):
                    resultMatrix = results[i]
                    file.write(f"Formula {i+1}: R{i+1} = {formula}\n\n")
                    file.write(f"Resultado de Formula {i+1} (R{i+1}):\n")
                    file.write("Resultado" + str(i+1) + " = {\n")
                    file.write(self._formatMatrixToString(resultMatrix, addBraces=False, addPipe=True))
                    file.write("\n}\n\n")
                file.write("\n")
        except Exception as error:
            createLogFile(self.fileManager, error, error.__traceback__, error)
            return None

    def writeSystemsAndSolutions(self, augmentedSystems: list[np.ndarray], solutions: list):
        """
        Escribe los sistemas aumentados y la información de los objetos Point como solución.
        solutions debe ser una lista de objetos Point (uno por sistema).
        """
        try:
            if len(augmentedSystems) != len(solutions):
                raise ValueError("La lista de matrices de sistemas y soluciones debe tener el mismo tamano.")

            with open(self.reportFile, "a") as file:
                file.write("--- RESOLUCION DE SISTEMAS POR GAUSS-JORDAN ---\n\n")

                for i, system in enumerate(augmentedSystems):
                    point_solution = solutions[i]
                    variables = ['x', 'y', 'z']

                    file.write(f"Sistema {i+1}:\n")

                    for row_data in system:
                        equation_parts = []
                        first_term_coeff = self._formatValue(row_data[0])
                        if first_term_coeff != "0":
                            equation_parts.append(f"{first_term_coeff}{variables[0]}")

                        for j in range(1, len(row_data) - 1):
                            coeff = row_data[j]
                            if coeff == 0:
                                continue

                            formatted_coeff = self._formatValue(abs(coeff))
                            sign = " + " if coeff > 0 else " - "

                            if formatted_coeff == "1":
                                formatted_coeff = ""

                            equation_parts.append(f"{sign}{formatted_coeff}{variables[j]}")

                        equation = "".join(equation_parts).strip()
                        if row_data[0] < 0:
                            equation = f"-{equation}"

                        result = self._formatValue(row_data[-1])
                        file.write(f"  {equation} = {result}\n")

                    file.write("\n")

                    file.write(f"Matriz Aumentada del Sistema {i+1}:\n")
                    file.write(self._formatMatrixToString(system, addPipe=True) + "\n\n")

                    file.write(f"Solucion del Sistema {i+1}:\n")
                    # Mostrar la información relevante del objeto Point
                    if hasattr(point_solution, 'getName') and hasattr(point_solution, 'getPosition'):
                        name = point_solution.getName()
                        pos = point_solution.getPosition()
                        pos_str = ', '.join([self._formatValue(x) for x in pos])
                        file.write(f"Punto solucion: {name} = ({pos_str})\n\n")
                    else:
                        file.write("[Error: El objeto de solucion no es un Point valido]\n\n")
                file.write("\n")
        except Exception as error:
            createLogFile(self.fileManager, error, error.__traceback__, error)
            return None

    def _formatValue(self, value):
        try:
            if value == int(value):
                return str(int(value))
            fraction = Fraction(value).limit_denominator(1000)
            if fraction.denominator == 1:
                return str(fraction.numerator)
            return str(fraction)
        except OverflowError:
            return f"{value:.3f}"
        except Exception as error:
            createLogFile(self.fileManager, error, error.__traceback__, "format_value")
            return str(value)

    def writeDistancesBetweenPoints(self, points: list):
        try:
            if len(points) < 2:
                raise ValueError("Se necesitan al menos dos puntos para calcular distancias.")
            with open(self.reportFile, "a") as file:
                file.write("--- CALCULO DE DISTANCIAS ENTRE PUNTOS ---\n\n")
                file.write("Puntos Definidos:\n")
                for idx, point in enumerate(points):
                    pos_str = ', '.join(map(str, point.getPosition()))
                    file.write(f"Punto {point.getName()} = ({pos_str})\n")
                file.write("\n")
                uniqueDistances = set()
                for i in range(len(points)):
                    point1 = points[i]
                    for j in range(i + 1, len(points)):
                        point2 = points[j]
                        if hasattr(point1, 'distancesBetweenPoints') and point2.getName() in point1.distancesBetweenPoints:
                            distance = point1.distancesBetweenPoints[point2.getName()]
                        elif hasattr(point2, 'distancesBetweenPoints') and point1.getName() in point2.distancesBetweenPoints:
                            distance = point2.distancesBetweenPoints[point1.getName()]
                        else:
                            pos1 = np.array(point1.getPosition())
                            pos2 = np.array(point2.getPosition())
                            distance = np.linalg.norm(pos1 - pos2)
                        
                        if isinstance(distance, (int, float)) and np.isclose(distance, int(distance)):
                            formattedDistance = str(int(round(distance)))
                        else:
                            formattedDistance = self._formatValue(distance)
                            if formattedDistance.startswith('sqrt'):
                                pass
                            elif not formattedDistance.startswith('sqrt'):
                                formattedDistance = f"{distance:.3f}"
                        file.write(f"Distancia entre {point1.getName()} y {point2.getName()}: d({point1.getName()}, {point2.getName()}) = {formattedDistance}\n")
                        uniqueDistances.add(formattedDistance)
                file.write("\nConjunto de Distancias Unicas:\n")
                distancesSetNotation = ", ".join(sorted(list(uniqueDistances)))
                file.write(f"D = {{ {distancesSetNotation} }}\n\n")
        except Exception as error:
            createLogFile(self.fileManager, error, error.__traceback__, self.reportFile)
            return None
