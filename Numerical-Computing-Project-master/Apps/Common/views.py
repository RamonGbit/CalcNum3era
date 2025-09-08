from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import io
from .utils import generaPuntos, create_plot_buffer, createLinePlotResponser


@require_http_methods(["POST"])
@csrf_exempt
def generate_line_points(request):
   #funcion http que recibe parametros de la pendiente en json
    try:
        data = json.loads(request.body)
        
        slope = data.get('slope')
        intercept = data.get('intercept')
        x_values = data.get('x_values', [])
        
        # Generar los puntos
        points = generaPuntos(slope, intercept, x_values)
        
        return JsonResponse({
            'success': True,
            'points': points,
            'message': f'Se generaron {len(points)} puntos exitosamente'
        })
        
    except (TypeError, ValueError) as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor'
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def create_plot_image(request):
    try:
        data = json.loads(request.body)
        
        points = data.get('points', [])
        plot_type = data.get('plot_type', 'scatter')
        title = data.get('title', 'Gráfica de Puntos')
        
        # Convertir puntos a tuplas si vienen como listas, para el throw error
        if points and isinstance(points[0], list):
            points = [tuple(point) for point in points]
        
        # Crear la grafica
        buffer = create_plot_buffer(points, plot_type=plot_type, title=title)
        
        # Retornar la imagen
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'inline; filename="grafica.png"'
        
        return response
        
    except (TypeError, ValueError) as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Error al crear la gráfica'
        }, status=500)


def line_regression_view(request):
 
    if request.method == 'POST':
        try:
            # parametros del form
            slope = float(request.POST.get('slope', 1))
            intercept = float(request.POST.get('intercept', 0))
            x_start = float(request.POST.get('x_start', -10))
            x_end = float(request.POST.get('x_end', 10))
            x_step = float(request.POST.get('x_step', 1))
            
            # Generar valores de x
            x_values = []
            x = x_start
            while x <= x_end:
                x_values.append(x)
                x += x_step
            
            # Generar puntos
            points = generaPuntos(slope, intercept, x_values)
            
            # Crear grafica
            buffer = createLinePlotResponser(
                points, 
                title=f'Recta: y = {slope}x + {intercept}'
            )
            
            # Convertir buffer a base64 para mostrar en HTML
            import base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            context = {
                'slope': slope,
                'intercept': intercept,
                'points': points[:10],  # muestra solo los primeros 10 puntos
                'total_points': len(points),
                'image_data': image_base64,
                'success': True
            }
            
        except (ValueError, TypeError) as e:
            context = {
                'error': f'Error en los parámetros: {str(e)}',
                'success': False
            }
        
        except Exception as e:
            context = {
                'error': 'Error interno del servidor',
                'success': False
            }
    
    else:
        # GET request 
        context = {
            'slope': 1,
            'intercept': 0,
            'x_start': -10,
            'x_end': 10,
            'x_step': 1
        }
    
    return render(request, 'regression/line_plot.html', context)


# API endpoint
@require_http_methods(["POST"])
@csrf_exempt
def generate_and_plot(request):
  
    try:
        data = json.loads(request.body)
        
        slope = data.get('slope')
        intercept = data.get('intercept')
        x_values = data.get('x_values', [])
        plot_type = data.get('plot_type', 'line')
        title = data.get('title', f'Recta: y = {slope}x + {intercept}')
        
        # Generar puntos
        points = generaPuntos(slope, intercept, x_values)
        
        # Crear grafica
        buffer = create_plot_buffer(points, plot_type=plot_type, title=title)
        
        # Convertir a base 64
        import base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return JsonResponse({
            'success': True,
            'points': points,
            'image_base64': image_base64,
            'total_points': len(points),
            'equation': f'y = {slope}x + {intercept}'
        })
        
    except (TypeError, ValueError) as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor'
        }, status=500)