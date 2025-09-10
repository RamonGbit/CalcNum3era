import os
import numpy as np
import matplotlib.pyplot as plt

class DataDivision():
    def __init__(self, filepath, separador='#'):
        if not filepath or not isinstance(filepath, str):
            raise ValueError("La ruta del archivo no puede estar vacía y debe ser un string.")
        if not isinstance(separador, str):
            raise TypeError("El separador debe ser un string.")
        self.filepath = filepath
        self.separador = separador
        self.muestra = None
        self.submuestras = None

    def setRandomSample(self, muestra_size=250000):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            datos = np.fromiter((int(x) for x in f.read().split(self.separador)), dtype=np.int32)
        self.muestra = np.random.choice(datos, muestra_size, replace=False)
        return self.muestra

    def setSplitInFive(self, arr):
        if len(arr) != 250000:
            raise ValueError("El arreglo debe tener exactamente 250,000 datos.")
        self.submuestras = [arr[i*50000:(i+1)*50000] for i in range(5)]
        return self.submuestras

    def setSplitRandomArray(self, arr):
        if arr.size != 50000:
            raise ValueError("El arreglo debe tener exactamente 50,000 datos.")
        arr_shuffled = np.random.permutation(arr)
        mitad = arr.size // 2
        arreglo1 = arr_shuffled[:mitad]
        arreglo2 = arr_shuffled[mitad:]
        return arreglo1, arreglo2

    def getGraphic(self, arr1, arr2, i):
        plt.figure()
        plt.scatter(arr1, arr2, s=1, alpha=0.5)
        m, b = np.polyfit(arr1, arr2, 1)
        x_vals = np.array([arr1.min(), arr1.max()])
        y_vals = m * x_vals + b
        plt.plot(x_vals, y_vals, color='red', linewidth=2, label='Tendencia')
        plt.title("Gráfico de dispersión: Arreglo 1 vs Arreglo 2")
        plt.xlabel("Arreglo 1 (X)")
        plt.ylabel("Arreglo 2 (Y)")
        plt.legend()

        output_dir = "Apps\DataProcessor\IMG"
        output_filename = "graphic" + str(i) + ".png"
        os.makedirs(output_dir, exist_ok=True)
        full_output_path = os.path.join(output_dir, output_filename)
        plt.savefig(full_output_path)
        plt.close()

        return full_output_path
    
    def getBestFitLine(self, x, y):
        m, b = np.polyfit(x, y, 1)
        text= f"Ecuación de la recta de mejor ajuste: y = {m:.4f}x + {b:.4f}"
        return text