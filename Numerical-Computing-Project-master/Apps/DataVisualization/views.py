from django.shortcuts import render
from Apps.Common.Composables.MatrixEquationGenerator import MatrixEquationGenerator
from django.http import JsonResponse
from Apps.NumericalMethods.Solvers.EquationSolvers.MatrixEquationSolver import MatrixEquationSolver
from Apps.Common.Composables.DataGenerate import archiveGenerator
from Apps.NumericalMethods.Solvers.MatrixOperators.SystemOfEquationsSolver import SystemOfEquationsSolver
from Apps.Common.Repositories.DataModels.Point import Point
from Apps.DataVisualization.Methods.GraphVisualizer import GraphVisualizer
from Apps.Common.Composables.MathReport import MathReport
from Apps.Common.Helpers.FileReaders.NumberScanner import NumberScanner
from datetime import datetime, timedelta
import numpy as np
from Apps.Common.Repositories.FileManager import FileManager

from .Methods.RandomGraphUtils import *

last_access_times = {}

def randomGraph(request):
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)
    try:
        client_ip = request.META.get('REMOTE_ADDR')
        current_time = datetime.now()

        if client_ip not in last_access_times:
            last_access_times[client_ip] = []
        
        last_access_times[client_ip] = [
            t for t in last_access_times[client_ip] if current_time - t < timedelta(minutes=1)
        ]

        if len(last_access_times[client_ip]) >= 5:
            alert_message = "Access limit exceeded: You can only visit this page 5 times per minute."
            return render(request, 'index.html', {'alert_message': alert_message})
        
        last_access_times[client_ip].append(current_time)

        generator = archiveGenerator()
        equationSolver = MatrixEquationSolver()
        gaussSolver = SystemOfEquationsSolver()
        variableNames = ['A', 'B', 'C']

        matrixFiles: list[str] = generateMatrixFiles(generator, 3)
        MatrixEquationGenerator.generateComplexFormulas()
        report = MathReport(matrixFiles[0])

        matrixs: dict[str, np.ndarray] = loadMatrices(variableNames, matrixFiles)
        formulas: list[str] = loadFormulas("MatrixFormulas.txt")

        equationResults: list[np.ndarray] = resolveMatrixFormulas(equationSolver, formulas, matrixs)
        points: list[Point] = solvePoints(gaussSolver, equationResults, variableNames)
        setPointsGroup(points)
        image: str = GraphVisualizer.plotPointsAndDistances3D(points)
        
        report.writeOriginalMatrices(matrixs)
        report.writeFormulasAndResults(formulas, equationResults)
        report.writeSystemsAndSolutions(equationResults, points)
        report.writeDistancesBetweenPoints(points)
        

        plot_results = [p.toDict() for p in points]
        context = {
            'plot_url': image,
            'plot_results': plot_results, 
            'matrices': matrixs,
            'formulas': formulas,
            'equationResults': equationResults
        }
        return render(request, 'index.html', context)
    
    except Exception as error:
        from errors import createLogFile
        # Necesitarías pasar un objeto manager aquí o manejarlo de otra manera
        createLogFile(fileManager   , error, error.__traceback__, "randomGraph view")
        
        # Retornar una respuesta de error apropiada
        context = {
            'error_message': 'An error occurred while processing your request. Please try again later.'
        }
        return render(request, 'error.html', context, status=500)


