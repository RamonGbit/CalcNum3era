import matplotlib.pyplot as plt
import numpy as np

class InterpolacionLagrange:
    def __init__(self, x, y):
        """
        el objeto lo inicias con los datos x ^ y como arrays de numpy.

        Args:
            x (np.array): array de numpy ccon las x.
            y (np.array): array de numpy con las y.
        """
        self.x = x
        self.y = y

    def metodoLagrange(self, puntoX):
        """
        calculo del valor interpolado en el punto x

        Args:
            puntoX (float): El punto x en el que se desea interpolar.

        Returns:
            float: el valor interpolado.
        """
        polinomio = 0
        n = len(self.x)

        for i in range(n):
            termino = 1
            for j in range(n):
                if i != j:
                    termino *= (puntoX - self.x[j]) / (self.x[i] - self.x[j])
            polinomio += termino * self.y[i]
        return polinomio

    def obtenerResultados(self):
        """
        este genera los puntos x e y para graficar la interpolacion.

        Returns:
            tuple: los 2 arrays de numpy con los valores de x ^ y para la grafica.
        """
        minX = np.min(self.x)
        maxX = np.max(self.x)
        
        # aca genera 100 puntos entre el minimo y maximo de x espaciados uniformemente
        valoresX = np.linspace(minX, maxX, 100)
        valoresY = [self.metodoLagrange(x) for x in valoresX]

        return valoresX, valoresY

    def graficar(self, nombreArchivo='interpolacion_lagrange.png'):
        """
        genera la grafica con matplotlib y la guarda en un archivo PNG.

        Args:
            nombreArchivo (str): el nombre del PNG.
        """
        valoresX, valoresY = self.obtenerResultados()

        plt.figure(figsize=(10, 6))
        plt.scatter(self.x, self.y, label='Datos Originales', color='blue')
        plt.plot(valoresX, valoresY, 'r-', label='Interpolación de Lagrange')
        plt.ylabel('Valores Y')
        plt.xlabel('Valores X')
        plt.title('Interpolación Polinómica de Lagrange')
        plt.legend()
        plt.grid(True)
        
        # Guarda la figura en un archivo PNG
        plt.savefig(nombreArchivo)
        print(f"Gráfica guardada como '{nombreArchivo}'")
        plt.close()

# pueden usar un dic asi 
datos = {
    0: 21.9, 1: 21.6, 2: 21.9, 3: 22.0, 4: 22.3, 5: 21.8, 6: 20.9,
    7: 21.1, 8: 21.6, 9: 21.2, 10: 21.7, 11: 22.2, 12: 22.3, 13: 21.7,
    14: 22.3, 15: 22.8, 16: 24.0, 17: 22.8, 18: 22.8, 19: 22.8, 20: 24.4,
    21: 24.8, 22: 23.7, 23: 23.7, 24: 23.4, 25: 22.7, 26: 22.7, 27: 22.9,
    28: 23.1, 29: 23.6, 30: 22.4, 31: 21.9,
}
# y filtrarlos asi a np, o bueno pueden simplemente usar arrays de numpy directamente
xOriginal = np.array(list(datos.keys()))
yOriginal = np.array(list(datos.values()))

# elegir cuantos puntos usar para la interpolacion
cantidadPuntos = 7
xSeleccionados = xOriginal[:cantidadPuntos]
ySeleccionados = yOriginal[:cantidadPuntos]


# creando la instancia y graficando
lagrange = InterpolacionLagrange(xSeleccionados, ySeleccionados)
lagrange.graficar()