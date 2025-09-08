import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from io import BytesIO
import base64
from Apps.Common.Repositories.DataModels.Point import Point
from matplotlib.lines import Line2D
import traceback
from datetime import datetime
from random import randint
from typing import Any
from Apps.Common.Repositories.FileManager import FileManager

class GraphVisualizer:

    @staticmethod
    def plotPointsAndDistances3D(pointsList):
        path = ".\Apps\Common\Repositories\Errors"
        fileManager = FileManager(path)
        try:
            fig = plt.figure(figsize=(12, 10))
            ax = fig.add_subplot(111, projection='3d')
            
            pointStyles = {
                'A': {'color': 'red', 'marker': 'o', 'label': 'Punto A'},
                'B': {'color': 'blue', 'marker': '^', 'label': 'Punto B'},
                'C': {'color': 'green', 'marker': 's', 'label': 'Punto C'}
            }
            
            points = list(pointsList)
            
            plottedTypes = set()
            for point in points:
                x, y, z = point.getPosition()
                pointType = point.getName()[0]
                style = pointStyles.get(pointType, {'color': 'gray', 'marker': 'o', 'label': f'Punto {pointType}'})
                
                if pointType not in plottedTypes:
                    ax.scatter(x, y, z, c=style['color'], marker=style['marker'], s=100, label=style['label'])
                    plottedTypes.add(pointType)
                else:
                    ax.scatter(x, y, z, c=style['color'], marker=style['marker'], s=100)
                
                ax.text(x, y, z, f'  {point.getName()}', fontsize=10)
            
            for i, point1 in enumerate(points):
                for point2 in points[i+1:]:
                    x1, y1, z1 = point1.getPosition()
                    x2, y2, z2 = point2.getPosition()
                    distance = point1.calculateDistance(point2)
                    
                    ax.plot([x1, x2], [y1, y2], [z1, z2], 'k--', alpha=0.5)
                    midX, midY, midZ = (x1+x2)/2, (y1+y2)/2, (z1+z2)/2
                    ax.text(midX, midY, midZ, f'{distance:.2f}', backgroundcolor='white', fontsize=8)
            
            ax.set_title('Visualización 3D de Puntos y Distancias', pad=20)
            ax.set_xlabel('Eje X')
            ax.set_ylabel('Eje Y')
            ax.set_zlabel('Eje Z')
            ax.legend()
            ax.view_init(elev=25, azim=45)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            buffer.seek(0)
            
            imageBase64 = base64.b64encode(buffer.read()).decode('utf-8')
            return f"data:image/png;base64,{imageBase64}"
        
        except Exception as error:
            from errors import createLogFile
            createLogFile(fileManager   , error, error.__traceback__, error)
            return None
