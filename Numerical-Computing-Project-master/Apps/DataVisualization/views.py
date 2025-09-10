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
from Apps.DataProcessor.DataExtractor.extractor import start_process
from Apps.DataProcessor.DataExtractor.extractor import encode_image_to_base64
from .Methods.RandomGraphUtils import *
from Apps.Common.Repositories.Errors.NumberofErrors import contador
import base64
from Apps.Documentation.pdf_generator import generate_pdf

last_access_times = {}
errors = []

def randomGraph(request):
    global errors
    path = "Apps\Common\Repositories\Errors"
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
            scatter_paths, linearPath, cubicPath, lagrangePath, equation = start_process()
            scatter_images = [encode_image_to_base64(p) for p in scatter_paths]
            linear_img = encode_image_to_base64(linearPath)
            cubic_img = encode_image_to_base64(cubicPath)
            lagrange_img = encode_image_to_base64(lagrangePath)
            numberOfErrors=contador("Apps\Common\Repositories\Errors\error.log")
            
            errores_por_iteracion = []
            if errors:
                errores_por_iteracion.append(errors[0])
                for i in range(1, len(errors)):
                    errores_por_iteracion.append(errors[i] - errors[i-1])
            
            normalDistributionData = getNormalDistributionData(errores_por_iteracion)
            
            # Construir la lista de iteraciones
            iteraciones = []
            nombres = [
                "Primera iteración", "Segunda iteración", "Tercera iteración",
                "Cuarta iteración", "Quinta iteración"
            ]
            for i in range(min(len(scatter_paths), len(equation), len(errores_por_iteracion))):
                # Codificar imagen a base64
                with open(scatter_paths[i], "rb") as imgf:
                    imagen_final = base64.b64encode(imgf.read()).decode("utf-8")
                iteraciones.append({
                    "nombre": nombres[i] if i < len(nombres) else f"Iteración {i+1}",
                    "puntos": 50000,
                    "recta": equation[i],
                    "imagen": imagen_final,
                    "errores": errores_por_iteracion[i]
                })
            content = {
                "iteraciones" : iteraciones,
                "interpolaciones": [
                    {
                        "tipo_interpolacion" : "Lineal",
                        "total_puntos" : 2000000,
                        "imagen_interpolacion" : linear_img
                    },
                    {
                        "tipo_interpolacion" : "Cubica",
                        "total_puntos" : 2000000,
                        "imagen_interpolacion" : cubic_img
                    },
                    {
                        "tipo_interpolacion" : "Lagrange",
                        "total_puntos" : 2000000,
                        "imagen_interpolacion" : lagrange_img
                    }
                ],
                "sumatoria": normalDistributionData["sumatoria"],
                "promedio": normalDistributionData["promedio"],
                "media": normalDistributionData["media"],
                "desviacion": normalDistributionData["desviacion"],
                "rango_68": normalDistributionData["rango_68"],
                "rango_95": normalDistributionData["rango_95"],
                "rango_98": normalDistributionData["rango_98"],
                "imagen_distribucion": normalDistributionData["imagen_distribucion"]
                }
            generate_pdf(content)
            context = {
                'alert_message': "Access limit exceeded: You can only visit this page 5 times per minute.",
                'scatter_images': scatter_images,
                'linear_img': linear_img,
                'cubic_img': cubic_img,
                'lagrange_img': lagrange_img,
                'iteraciones': iteraciones,
                'normalDistributionData': normalDistributionData,
            }
            errors = []
            return render(request, 'graph.html', context)
        
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

        numberOfErrors=contador("Apps\Common\Repositories\Errors\error.log")
        if numberOfErrors:
            errors.append(numberOfErrors)
        else:
            errors.append(0)
        
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
        
        # Retornar una respuesta de error apropiada, mostrando el error real
        import traceback
        tb = traceback.format_exc()
        context = {
            'error_message': f"Ocurrió un error: {type(error).__name__}: {str(error)}",
            'traceback': tb
        }
        return render(request, 'error.html', context, status=500)


