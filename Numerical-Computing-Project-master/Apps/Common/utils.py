import logging
import sys
import traceback
from datetime import datetime

def createLogFile(log_filename: str = "app_error.log"):
    """
    Configura el sistema de logging para registrar errores y excepciones no controladas.
    El log incluye timestamp, mensaje, módulo y stack trace.
    """
    logging.basicConfig(
        level=logging.ERROR,
        filename=log_filename,
        filemode='a',
        format='%(asctime)s | %(levelname)s | %(module)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        # Formato de stack trace
        stack = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logging.error(f"Excepción no controlada: {exc_value}\nStack trace:\n{stack}")

    sys.excepthook = handle_exception
import io
import matplotlib 
matplotlib.use('Agg') #usuario backend
import matplotlib.pyplot as plt
from typing import List, Tuple, Union #cambiar por las implementadas de 0 (no se si hay, no revise)
import numpy as pai

def generaPuntos(slope: Union[int,float], intercept: Union[int,float], xArray: List[Union[int, float]])-> List[Tuple[float, float]]:
    #esta mierda hace la generacion de puntos en tuplas(para NO modificar despues)}

    if not isinstance(slope, (int,float)): #COMPROBACIONES de datos
        raise TypeError/(f"La pendiente debe tener valor numerico")
    
    if not isinstance(intercept, (int,float)):
        raise TypeError(F"El intercepcion deeb ser numerico")
    
    if not xArray:
        raise ValueError("El array x no puede estar vacio")
    

    for i, x in enumerate(xArray): #enumera cada fila del array para verificar que el valor coincida
        if not isinstance(x, (int,float)):
            raise ValueError(f"El valor de x en la posicion {i} no es numerico")
        
    puntos= [] #arreglo para guardar todas las tuplas 
    for x in xArray:
        y= slope*x + intercept #ejemplo de ecuacion de la recta
        puntos.append((float(x), float(y)))

    return puntos



def create_plot_buffer(puntosArray: List[Tuple[Union[int, float], Union[int, float]]], plotType: str = 'scatter', titulo: str = 'Grafica de Puntos',etiquetaX: str = 'X',etiquetaY: str = 'Y') -> io.BytesIO:
    #crea la grafica teniendo en cuenta los puntos y se guarda en un buffer
    #todo esto segun lo que dice el issue


    if not puntosArray:
        raise ValueError("EL array no puede estar vacio")
    

    valoresX=[]
    valoresY=[]

    for i, punto in enumerate(puntosArray):
        #funcion que valida que cada elemento punto sea la tupla valida
        if not isinstance(punto, tuple) or len(punto)!=2:
            raise TypeError(f"El punto en la posicion {i} debe ser tupla con 2 elementos")
        
        x, y = punto

        if not isinstance(x,(int,float)) or not isinstance(y, (int,float)):
            raise ValueError(f"Los valores x e y en posiciones {i} deben ser numericos")
        
        valoresX.append(x)
        valoresY.append(y)


    plt.figure(figsize=(15,10)) #crea la grafica de plt


    if plotType.lower()=="line":
        plt.plot(valoresX,valoresY, marker="o", linestyle="-", color="blue", linewidth=2, markersize= 6)
    else:
        plt.scatter(valoresX,valoresY, alpha=0.7, s=50)


    #dimnensiones y titulos
    plt.tittle(titulo, fojtsize=16, fontweight="bold")
    plt.etiquetaX(etiquetaX, fontsize=14)
    plt.etiquetaY(etiquetaY, fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    #guarda la grafica y sus detalles en un byffer
    buffer= io.BytesIO()
    plt.savefig(buffer, format="png", dpi= 300, bbox_inches="tight")
    buffer.seek(0) #para el pointer al inicio



    plt.clf()
    plt.close() #limpiaa y cierra el figure para liberar memoria(pa hacer feliz a marrugo)

    return buffer



def createLinePlotResponser(puntosArray: List[Tuple[Union[int, float], Union[int, float]]], titulo: str = 'Recta de Mejor ajuste') -> io.BytesIO:

    return create_plot_buffer(puntosArray, plotType='line', titulo=titulo, etiquetaX='X', etiquetaY='Y')


"""pruebas rapidas 
if __name__=="__main__":
    #pruebas rapidas
    slope=2
    intercept=3
    xArray=[1,2,3,4,5]

    puntos=generaPuntos(slope, intercept, xArray)
    print(puntos)

    buffer=createLinePlotResponser(puntos)
    with open("test_plot.png", "wb") as f:
        f.write(buffer.getbuffer())
    print("Grafica guardada como test_plot.png")

"""
