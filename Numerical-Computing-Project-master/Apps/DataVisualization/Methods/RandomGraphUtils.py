import uuid
import numpy as np
from Apps.Common.Composables.DataGenerate import archiveGenerator
from Apps.Common.Repositories.DataModels.Point import Point  
from Apps.Common.Helpers.FileReaders.NumberScanner import NumberScanner
import os
from Apps.Common.Repositories.FileManager import FileManager
import matplotlib.pyplot as plt
import io
import base64

def generateMatrixFiles(generator: archiveGenerator, count: int) -> list[str]:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    try:
        numberScanner = NumberScanner()
        files = []
        for i in range(1, count + 1):
            serial = uuid.uuid4().hex[:8]
            filename = f"{serial}_matriz{i}_{serial}.txt"
            generator.setName(filename)
            generator.archiveDataGenerator(3, 4)
            numberScanner.scanAnalizeAndWriteResults(filename)
            files.append(filename)
        return files
    except Exception as error:
        from errors import createLogFile
        createLogFile(fileManager   , error, error.__traceback__, count)
        return None

def loadMatrices(variableNames: list[str], matrixFiles: list[str]) -> dict[str, np.ndarray]:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    try:
        data_dir = os.path.join(os.getcwd(), "Storage", "Data")
        matrices = {}
        for name, fname in zip(variableNames, matrixFiles):
            file_path = os.path.join(data_dir, fname)
            matrices[name] = np.loadtxt(file_path, delimiter='/')
        return matrices
    except Exception as error:
        from errors import createLogFile
        createLogFile(fileManager   , error, error.__traceback__, variableNames)
        return None


def loadFormulas(formulaFile: str) -> list[str]:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    try:
        data_dir = os.path.join(os.getcwd(), "Storage", "Data")
        file_path = os.path.join(data_dir, formulaFile)
        with open(file_path) as f:
            return [line.strip() for line in f.readlines()]
    except Exception as error:
        from errors import createLogFile
        createLogFile(fileManager   , error, error.__traceback__, formulaFile)
        return None

def resolveMatrixFormulas(equationSolver, formulas: list[str], matrices: dict[str, np.ndarray]) -> list[np.ndarray]:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    try:
        results = []
        for formula in formulas:
            result = equationSolver.solve(formula, matrices)
            results.append(result)
        return results
    except Exception as error:
        from errors import createLogFile
        createLogFile(fileManager   , error, error.__traceback__, formulas)
        return None

def solvePoints(gaussSolver, equationResults: list[np.ndarray], variableNames: list[str]) -> list[Point]:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    try:
        points = []
        for i, matrix in enumerate(equationResults):
            matrixCoefficient = matrix[:, :3]
            vectorIndependent = matrix[:, 3]
            gaussResult = gaussSolver.gaussJordanFullPivoting(matrixCoefficient, vectorIndependent)
            points.append(Point(variableNames[i], gaussResult))
        return points
    except Exception as error:
        from errors import createLogFile
        createLogFile(fileManager   , error, error.__traceback__, variableNames)
        return None

def setPointsGroup(points: list[Point]):
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    try:
        for point in points:
            point.setPointGroup(points)
    except Exception as error:
        from errors import createLogFile
        createLogFile(fileManager   , error, error.__traceback__, points)
        return None

def getNormalDistributionData(data: list[int]):
    data = np.array(data)
    mu = float(np.mean(data))
    sigma = float(np.std(data))

    rango_68 = {"inferior": mu - sigma, "superior": mu + sigma}
    rango_95 = {"inferior": mu - 2*sigma, "superior": mu + 2*sigma}
    rango_98 = {"inferior": mu - 3*sigma, "superior": mu + 3*sigma}

    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    y = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu)/sigma)**2)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, label=f'N({mu:.2f}, {sigma:.2f}²)')
    ax.hist(data, bins=30, density=True, alpha=0.5, color='skyblue', label='Datos')
    ax.set_title('Distribución Normal Ajustada')
    ax.set_xlabel('Valor')
    ax.set_ylabel('Densidad')
    ax.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    imagen_final = base64.b64encode(buf.read()).decode('utf-8')

    return {
        "media": round(mu, 2),
        "desviacion": round(sigma, 2),
        "rango_68": {"inferior": round(rango_68["inferior"], 2), "superior": round(rango_68["superior"], 2)},
        "rango_95": {"inferior": round(rango_95["inferior"], 2), "superior": round(rango_95["superior"], 2)},
        "rango_98": {"inferior": round(rango_98["inferior"], 2), "superior": round(rango_98["superior"], 2)},
        "imagen_distribucion": imagen_final,
        "promedio": round(mu, 2),
        "sumatoria": int(np.sum(data))
    }

