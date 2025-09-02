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
    - **NumericalMethods/**: Métodos numéricos y algoritmos para la resolución de ecuaciones y operaciones matriciales.

- **Storage/**: Carpeta para archivos de entrada (matrices, fórmulas) y resultados generados (reportes, logs, soluciones).
    - **Data/**: Archivos de datos de entrada y fórmulas.
    - **Results/**: Resultados, reportes y logs generados por el sistema.

- **NumericalComputingProject/**: Configuración principal de Django (settings, urls, wsgi/asgi).
- **manage.py**: Script de administración y entrada para comandos Django.

### Flujo General

1. **Generación de Datos:** Se crean matrices aleatorias y se almacenan en archivos.
2. **Procesamiento Numérico:** Se resuelven sistemas de ecuaciones y se analizan los números.
3. **Visualización:** Se grafican los puntos y distancias en 3D.
4. **Reporte:** Se generan archivos formales con todos los resultados y análisis.
5. **Interfaz Web:** El usuario accede a la URL principal para ver la gráfica y los resultados.

---

## ⚙️ Instalación y Ejecución

Siga estos pasos para configurar y ejecutar la aplicación en su entorno local:

### 1. Pre-requisitos

- **Python 3.9 o superior**
- **pip** (gestor de paquetes de Python)
- Se recomienda el uso de `virtualenv` para aislar dependencias.

### 2. Clonar el Repositorio

```bash
git clone https://github.com/Abisaac1809/Numerical-Computing-Project.git
cd Numerical-Computing-Project
```

### 3. Crear y Activar un Entorno Virtual

```bash
# Instalar virtualenv si no lo tiene
pip install virtualenv

# Crear el entorno virtual
virtualenv env

# Activar el entorno virtual (Windows)
.\env\Scripts\activate
# En macOS/Linux
# source env/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Migrar la Base de Datos (solo la primera vez)

```bash
python manage.py migrate
```

### 6. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

---

## 🌐 Acceso a la Aplicación y Visualización de la Gráfica

Una vez iniciado el servidor, acceda desde su navegador a:

```
http://localhost:8000/dataVisualization/randomGraph/
```

En esta URL podrá visualizar la gráfica 3D de puntos generados aleatoriamente, junto con los resultados numéricos y análisis detallados. Cada recarga genera nuevos datos y resultados.

---

## 🛠️ Tecnologías Utilizadas

- **Python** (>=3.9)
- **Django** (5.2.4)
- **NumPy** (2.2.6)
- **Matplotlib** (3.10.3)
- **SQLite** (base de datos por defecto de Django)

Consulte el archivo `requirements.txt` para la lista completa de dependencias.

---

## 📁 Estructura de Carpetas (Resumen)

```text
Numerical-Computing-Project/
├── Apps/
│   ├── Common/           # Utilidades, modelos y helpers compartidos
│   ├── DataVisualization/ # Visualización y gráficas
│   └── NumericalMethods/  # Métodos numéricos y algoritmos
├── Storage/
│   ├── Data/             # Archivos de entrada y fórmulas
│   └── Results/          # Resultados y reportes generados
├── NumericalComputingProject/ # Configuración principal Django
├── manage.py             # Script de administración
└── requirements.txt      # Dependencias del proyecto
```

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.

