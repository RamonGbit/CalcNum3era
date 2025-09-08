from .models import Iteracion

def get_last_five_iterations_m2m():
    """
    Recupera los datos de las últimas 5 iteraciones usando la nueva estructura Many-to-Many.
    """
    try:
        print("Recuperando las últimas 5 iteraciones desde la base de datos...")
        # 1. Obtenemos las últimas 5 iteraciones. El 'ordering' en el modelo ya las trae así.
        iteraciones = Iteracion.objects.all()[:5]

        # 2. Usamos 'prefetch_related' para cargar todos los puntos de estas 5 iteraciones
        # en una sola consulta adicional, lo cual es muy eficiente.
        iteraciones = iteraciones.prefetch_related('puntos')
        
        resultado_final = []
        for iteracion in iteraciones:
            # 3. Para cada iteración, creamos la lista de tuplas (x, y)
            puntos_de_la_iteracion = [
                (punto.coordenada_x, punto.coordenada_y)
                for punto in iteracion.puntos.all()
            ]
            resultado_final.append(puntos_de_la_iteracion)
        
        print("Recuperación completada.")
        return resultado_final

    except Exception as e:
        print(f"Error al conectar o consultar la base de datos: {e}")
        return [] # Retornar una lista vacía en caso de error