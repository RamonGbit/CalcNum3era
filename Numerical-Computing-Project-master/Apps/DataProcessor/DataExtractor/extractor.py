from Apps.DataProcessor.DataExtractor.DataDivision import DataDivision
from Apps.DataProcessor.DataExtractor.Interpolate import Interpolator
import numpy as np
import base64

def start_process():
    archivo = ".\Apps\DataProcessor\DataExtractor\Data\datos_generados.txt"
    data_divider = DataDivision(archivo, "#")
    muestra = data_divider.setRandomSample(250000)
    submuestras = data_divider.setSplitInFive(muestra)
    equation = []
    data_list = []
    i=0
    path=[]
    for submuestra in submuestras:
        arr1, arr2 = data_divider.setSplitRandomArray(submuestra)
        path.append(data_divider.getGraphic(arr1, arr2, i))
        i+=1
        print(i)
        orden = np.argsort(arr1)
        x = arr1[orden]
        y = arr2[orden]
        x_rounded = np.round(x, 0)
        y_rounded = np.round(y, 0)
        x_unique, idx_unique = np.unique(x_rounded, return_index=True)
        y_unique = y_rounded[idx_unique]
        data_list.append((x_unique, y_unique))
        equation.append(data_divider.getBestFitLine(x, y))
    interpolador = Interpolator(data_list)
    linarPath=interpolador.plot_interpolation(0, kind='linear')
    cubicPath=interpolador.plot_interpolation(0, kind='cubic')
    lagrangePath=interpolador.plot_interpolation(0, kind='lagrange')
    return path, linarPath, cubicPath, lagrangePath, equation 

def encode_image_to_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error leyendo imagen {path}: {e}")
        return ""
