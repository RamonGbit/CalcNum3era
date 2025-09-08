from .models import IterationRun

def get_last_five_iterations():
    """
    Se conecta a la base de datos y recupera los puntos (X, Y) de las últimas
    cinco IterationRun registradas.

    Returns:
        list[list[tuple[int, int]]]:
        Un arreglo de arreglos de tuplas. Cada arreglo interno representa
        una iteración y contiene las tuplas (x, y) de sus puntos.
        Retorna una lista vacía si no hay iteraciones o en caso de error.
    """
    print("Intentando obtener las últimas 5 iteraciones de la base de datos...")
    try:
        # Recupera las últimas 5 iteraciones usando optimización 'prefetch_related'
        last_five_runs = IterationRun.objects.prefetch_related('data_points').all()[:5]

        if not last_five_runs:
            print("No se encontraron iteraciones en la base de datos.")
            return []

        # Procesa los datos para organizarlos en el formato requerido
        all_iterations_data = []
        for run in last_five_runs:
            iteration_points = [
                (point.x_value, point.y_value) for point in run.data_points.all()
            ]
            all_iterations_data.append(iteration_points)
        
        print(f"Se recuperaron {len(all_iterations_data)} iteraciones exitosamente.")
        return all_iterations_data

    except Exception as e:
        # Manejo de errores de conexión o consulta
        print(f"Error al acceder a la base de datos: {e}")
        return []

