# Linear Regression Solver

## Descripción
Implementación de regresión lineal usando el método de mínimos cuadrados para calcular la recta de mejor ajuste.

## Uso

```python
from Apps.NumericalMethods.Solvers.LinearRegressionSolver import LinearRegressionSolver

# Crear instancia del solver
solver = LinearRegressionSolver()

# Datos de ejemplo
x_values = [1, 2, 3, 4, 5]
y_values = [2, 4, 6, 8, 10]

# Calcular regresión lineal
result = solver.calculateLinearRegression(x_values, y_values)

# Obtener pendiente e intercepto
pendiente = result['slope']
intercepto = result['intercept']

print(f"Pendiente: {pendiente}")
print(f"Intercepto: {intercepto}")
```

## Métodos

### `calculateLinearRegression(x_values, y_values)`
- **Parámetros**: 
  - `x_values`: Array de valores de X
  - `y_values`: Array de valores de Y
- **Retorna**: Diccionario con 'slope' (pendiente) y 'intercept' (intercepto)
- **Excepciones**: `NumberIsInvalid` si los datos no son válidos

## Validaciones
- Los arrays deben tener la misma longitud
- Debe haber al menos 2 puntos
- No todos los valores de X pueden ser iguales
- Los arrays no pueden estar vacíos
