from django.shortcuts import render
from django.http import HttpResponse
import os
from datetime import datetime, timedelta
import numpy as np
from Apps.Common.Helpers.DataProcessors.DataSetManager import DataSetManager
from .models import Punto, Iteracion
from Apps.Common.Composables.MatrixEquationGenerator import MatrixEquationGenerator
from Apps.NumericalMethods.Solvers.EquationSolvers.MatrixEquationSolver import MatrixEquationSolver
from Apps.Common.Composables.DataGenerate import archiveGenerator
from Apps.NumericalMethods.Solvers.MatrixOperators.SystemOfEquationsSolver import SystemOfEquationsSolver
from Apps.Common.Repositories.DataModels.Point import Point as PointAntiguo
from Apps.DataVisualization.Methods.GraphVisualizer import GraphVisualizer
from Apps.Common.Composables.MathReport import MathReport
from .Methods.RandomGraphUtils import *


def process_and_save_iterations_m2m(request):
    """
    Orquesta el proceso usando la nueva estructura Many-to-Many.
    """
    try:
        ruta_raiz_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        nombre_archivo_datos = 'datos_generados.txt' 
        ruta_archivo_datos = os.path.join(ruta_raiz_proyecto, 'Storage', 'Data', nombre_archivo_datos)
        
        print("\n--- INICIANDO PROCESO CON ESTRUCTURA MANY-TO-MANY ---")
        manejador = DataSetManager(ruta_archivo_datos, separador='#')
        tamano_muestra = manejador.calcularTamanoMuestraIdeal(nivelConfianza=0.95, margenError=0.05)
        
        for i in range(5):
            print(f"\nProcesando Iteración {i+1}...")
            coordenadas_x, coordenadas_y = manejador.generarConjuntoDeCoordenadas(tamano_muestra)
            
            nueva_iteracion = Iteracion.objects.create(cantidad_errores=0) 
            
            puntos_para_asociar = []
            for x, y in zip(coordenadas_x, coordenadas_y):
                punto, created = Punto.objects.get_or_create(coordenada_x=x, coordenada_y=y)
                puntos_para_asociar.append(punto)
            
            nueva_iteracion.puntos.set(puntos_para_asociar)
            print(f"Iteración {i+1} guardada y asociada con {len(puntos_para_asociar)} puntos.")

        return render(request, 'index.html', {'status': 'Proceso Many-to-Many completado. Revisa la consola del servidor.'})

    except Exception as e:
        print(f"\nOcurrió un error general en la vista: {e}")
        return HttpResponse(f"Error: {e}", status=500)


last_access_times = {}

def randomGraph(request):
    """
    Lógica original del proyecto para la generación de matrices y gráficos 3D.
    """
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
    points: list[PointAntiguo] = solvePoints(gaussSolver, equationResults, variableNames)
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

