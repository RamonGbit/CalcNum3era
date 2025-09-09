import random
import math
import os
import numpy as np 

class DataSetManager:

    def __init__(self, rutaArchivo: str, separador: str = ','):
        if not rutaArchivo or not isinstance(rutaArchivo, str):
            raise ValueError("Error: La ruta del archivo debe ser una cadena de texto no vacía.")
        if not os.path.exists(rutaArchivo):
            raise FileNotFoundError(f"Error: El archivo no fue encontrado en la ruta: {rutaArchivo}")
        if not isinstance(separador, str) or len(separador) != 1:
            raise ValueError("Error: El separador debe ser un único carácter.")

        self._rutaArchivo = rutaArchivo
        self._separador = separador
        self._poblacionDatos = np.array([], dtype=int)
        self._poblacionCargada = False
        self._tamanoPoblacion = 0

    def _cargarYContarPoblacion(self):
        if self._poblacionCargada:
            return

        print(f"Cargando población del archivo (usando NumPy): {self._rutaArchivo}...")
        try:
            datos_temporales = []
            with open(self._rutaArchivo, 'r') as archivo:
                for linea in archivo:
                    lineaLimpia = linea.strip()
                    if not lineaLimpia:
                        continue
                    partes = lineaLimpia.split(self._separador)
                    for parte in partes:
                        valorStr = parte.strip()
                        if valorStr:
                            try:
                                datos_temporales.append(int(float(valorStr)))
                            except ValueError:
                                print(f"Advertencia: Se omitió valor no numérico '{valorStr}'")
            
            self._poblacionDatos = np.array(datos_temporales, dtype=int)
            self._tamanoPoblacion = self._poblacionDatos.size
            self._poblacionCargada = True
            print(f"Carga finalizada. Población total: {self._tamanoPoblacion} valores.")
        except Exception as e:
            print(f"Ocurrió un error inesperado al cargar la población: {e}")
            raise

    def getTamanoPoblacion(self) -> int:
        if not self._poblacionCargada:
            self._cargarYContarPoblacion()
        return self._tamanoPoblacion

    def calcularTamanoMuestraIdeal(self, nivelConfianza: float = 0.95, margenError: float = 0.01) -> int:
        if not (0 < nivelConfianza < 1 and 0 < margenError < 1):
            raise ValueError("Error: Nivel de confianza y margen de error deben estar entre 0 y 1.")
        
        if not self._poblacionCargada:
            self._cargarYContarPoblacion()
        
        if self._tamanoPoblacion == 0:
             return 0

        puntuacionesZ = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        Z = puntuacionesZ.get(nivelConfianza, 1.96)
        p = 0.5
        E = margenError
        tamanoMuestra = ((Z**2) * p * (1 - p)) / (E**2)
        
        if tamanoMuestra > self._tamanoPoblacion * 0.05:
            tamanoMuestra = tamanoMuestra / (1 + (tamanoMuestra - 1) / self._tamanoPoblacion)

        return math.ceil(tamanoMuestra)

    def generarConjuntoDeCoordenadas(self, tamanoMuestra: int) -> tuple[list[int], list[int]]:
        """
        Extrae una nueva muestra aleatoria de la población y la convierte en coordenadas X e Y.
        """
        if not self._poblacionCargada:
            self._cargarYContarPoblacion()

        if tamanoMuestra > self._tamanoPoblacion:
            raise ValueError(f"El tamaño de la muestra ({tamanoMuestra}) no puede ser mayor que la población total ({self._tamanoPoblacion}).")

        # 1. Extraer la muestra usando la función optimizada de NumPy (replace=False asegura que no se repitan valores)
        muestraActual = np.random.choice(self._poblacionDatos, size=tamanoMuestra, replace=False)
        
        # 2. Asignar coordenadas
        np.random.shuffle(muestraActual)
        
        numeroValores = muestraActual.size
        if numeroValores % 2 != 0:
            datosParaEmparejar = muestraActual[:-1]
        else:
            datosParaEmparejar = muestraActual
            
        puntoMedio = datosParaEmparejar.size // 2
        # Convertimos los arrays de NumPy a listas de Python para mantener la compatibilidad con el resto del código
        coordenadasX = datosParaEmparejar[:puntoMedio].tolist()
        coordenadasY = datosParaEmparejar[puntoMedio:].tolist()

        return coordenadasX, coordenadasY

