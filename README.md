<p align="center">
    <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python" />
    <img src="https://img.shields.io/badge/Django-5.2.4-green?logo=django" />
    <img src="https://img.shields.io/badge/Matplotlib-3.10.3-orange?logo=matplotlib" />
</p>

# Numerical Computing Project

Integración de herramientas matemáticas computacionales para resolver operaciones numéricas y visualizarlas de forma interactiva usando Python y Django.

---

## 🚀 Acerca del Proyecto

Esta aplicación web permite la generación, análisis y visualización de datos numéricos, resolviendo sistemas de ecuaciones lineales mediante el método de Gauss-Jordan y mostrando gráficas 3D de puntos generados aleatoriamente. El sistema está diseñado para ser robusto, trazable y fácil de usar, facilitando el estudio y la experimentación con métodos numéricos.

---

## ✨ Características Principales

- **Visualización Dinámica:** Gráficas 3D interactivas de puntos generados aleatoriamente.
- **Resolución de Sistemas Numéricos:** Implementación del método de Gauss-Jordan para sistemas de ecuaciones lineales.
- **Análisis Numérico Detallado:** Estudio de cifras significativas, validez y operaciones elementales de cada número.
- **Reportes Formales:** Generación automática de archivos con matrices originales, resultados, soluciones y distancias.
- **Trazabilidad y Registro de Errores:** Logging detallado de errores y resultados para auditoría y depuración.
- **Monitoreo de Precisión:** Cálculo y almacenamiento de errores relativos para evaluar la calidad de los resultados.
- **Interfaz Web Intuitiva:** Acceso centralizado a través de una URL para interactuar con todas las funcionalidades.

---

## 🏗️ Arquitectura del Proyecto

El proyecto está organizado en aplicaciones y módulos independientes, siguiendo buenas prácticas de Django y separación de responsabilidades:

### Estructura General

- **Apps/**: Contiene las aplicaciones Django principales del sistema.
    - **Common/**: Funcionalidades y utilidades compartidas.
        - **Composables/**: Generación de datos, reportes y utilidades de escritura de archivos.
        - **Helpers/**: Conversores, manejo de errores, lectores de archivos y utilidades auxiliares.
        - **Repositories/**: Modelos de datos matemáticos, errores calculados, números personalizados y estructuras de datos.
        - **Structures/**: Implementaciones de estructuras de datos como listas enlazadas, pilas y colas.
    - **DataVisualization/**: Lógica de visualización y generación de gráficas. Incluye métodos para graficar y utilidades para generar puntos aleatorios y matrices.