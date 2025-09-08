import random
import math
import os

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
        self._poblacionDatos = []
        self._poblacionCargada = False
        self._tamanoPoblacion = 0

    def _cargarYContarPoblacion(self):
        if self._poblacionCargada:
            return

        print(f"Cargando población del archivo: {self._rutaArchivo}...")
        try:
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
                                self._poblacionDatos.append(int(float(valorStr)))
                            except ValueError:
                                print(f"Advertencia: Se omitió valor no numérico '{valorStr}'")
            
            self._tamanoPoblacion = len(self._poblacionDatos)
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
        if not self._poblacionCargada:
            self._cargarYContarPoblacion()

        if tamanoMuestra > self._tamanoPoblacion:
            raise ValueError(f"El tamaño de la muestra ({tamanoMuestra}) no puede ser mayor que la población total ({self._tamanoPoblacion}).")

        muestraActual = random.sample(self._poblacionDatos, tamanoMuestra)
        
        random.shuffle(muestraActual)
        
        numeroValores = len(muestraActual)
        if numeroValores % 2 != 0:
            datosParaEmparejar = muestraActual[:-1]
        else:
            datosParaEmparejar = muestraActual
            
        puntoMedio = len(datosParaEmparejar) // 2
        coordenadasX = datosParaEmparejar[:puntoMedio]
        coordenadasY = datosParaEmparejar[puntoMedio:]

        return coordenadasX, coordenadasY