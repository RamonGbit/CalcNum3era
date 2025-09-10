import numpy as np
from scipy.interpolate import interp1d, BarycentricInterpolator
import matplotlib.pyplot as plt
import io
import os
import base64

class Interpolator:
    """
    Clase para realizar interpolaciones y graficar conjuntos de datos.

    Métodos principales:
    - interpolate(graph_idx, x_new, kind): Interpola los datos usando el método especificado ('linear', 'cubic', 'lagrange').
    - plot_interpolation(...): Genera y guarda una gráfica de interpolación para un conjunto de datos.
    - plot_all_interpolations(...): Genera y muestra todas las gráficas de interpolación.

    Atributos:
    - data_list: Lista de tuplas (x, y) con los datos de entrada para cada gráfica.
    - interpolators_linear: Interpoladores lineales para cada conjunto de datos.
    - interpolators_cubic: Interpoladores cúbicos para cada conjunto de datos.
    - interpolators_lagrange: Interpoladores de Lagrange para cada conjunto de datos.
    - _xs, _ys: Listas de los valores únicos de x e y para cada conjunto de datos.
    - max_global_lagrange_points: Máximo de puntos para interpolación de Lagrange global.
    - lagrange_sample_points: Número de puntos de muestra para Lagrange si hay demasiados puntos.
    """
    def __init__(self, data_list):
        
        if len(data_list) != 5:
            raise ValueError("Se requieren datos de exactamente 5 gráficas.")
        self.data_list = data_list
        
        self.interpolators_linear = []
        self.interpolators_cubic = []
        self.interpolators_lagrange = []  
        
        self._xs = []
        self._ys = []
        
        self.max_global_lagrange_points = 50
        
        self.lagrange_sample_points = 50
        self._create_interpolators()

    def _create_interpolators(self):
        for x, y in self.data_list:
            x = np.asarray(x)
            y = np.asarray(y)
            if x.size < 2:
                raise ValueError("Cada gráfica debe contener al menos 2 puntos para interpolar.")

            order = np.argsort(x)
            x_sorted = x[order]
            y_sorted = y[order]
            
            x_unique, idx_unique = np.unique(x_sorted, return_index=True)
            y_unique = y_sorted[idx_unique]

            f_linear = interp1d(x_unique, y_unique, kind='linear', fill_value="extrapolate")
            
            if x_unique.size >= 4:
                f_cubic = interp1d(x_unique, y_unique, kind='cubic', fill_value='extrapolate')
            else:
                f_cubic = interp1d(x_unique, y_unique, kind='linear', fill_value='extrapolate')

            
            if x_unique.size <= self.max_global_lagrange_points:
                try:
                    poly_lagrange = BarycentricInterpolator(x_unique, y_unique)
                except Exception:
                    poly_lagrange = None
            else:
                
                n = x_unique.size
                m = min(self.lagrange_sample_points, n)
                idx = np.linspace(0, n-1, m).astype(int)
                try:
                    poly_lagrange = BarycentricInterpolator(x_unique[idx], y_unique[idx])
                except Exception:
                    poly_lagrange = None

            self.interpolators_linear.append(f_linear)
            self.interpolators_cubic.append(f_cubic)
            self.interpolators_lagrange.append(poly_lagrange)
            self._xs.append(x_unique)
            self._ys.append(y_unique)

    def interpolate(self, graph_idx, x_new, kind='linear'):
        
        if kind == 'linear':
            return self.interpolators_linear[graph_idx](x_new)
        elif kind == 'cubic':
            return self.interpolators_cubic[graph_idx](x_new)
        elif kind == 'lagrange':
            poly = self.interpolators_lagrange[graph_idx]
            if poly is not None:
                return poly(x_new)
            
            xs = self._xs[graph_idx]
            ys = self._ys[graph_idx]
            return np.interp(x_new, xs, ys)
        else:
            raise ValueError("Tipo de interpolación no soportado: usa 'linear', 'cubic' o 'lagrange'.")

    def plot_interpolation(self, graph_idx, kind='linear', num_points=100, point_size=6, y_margin_frac=0.05, clip=True, ax=None, line_color=None, output_dir="Apps\DataProcessor\IMG"):
        x, y = self.data_list[graph_idx]
        x_new = np.linspace(np.min(x), np.max(x), num_points)
        y_new = self.interpolate(graph_idx, x_new, kind=kind)
        y_min, y_max = np.min(y), np.max(y)
        y_lo, y_hi = None, None
        if np.isfinite(y_min) and np.isfinite(y_max):
            span = y_max - y_min
            if span == 0:
                margin = max(abs(y_min) * 0.1, 1.0)
            else:
                margin = span * float(y_margin_frac)
            y_lo, y_hi = y_min - margin, y_max + margin
            if clip:
                y_new = np.clip(y_new, y_lo, y_hi)
        fig, ax = plt.subplots()
        default_colors = {
            'linear': 'yellow',
            'cubic': 'C1',
            'lagrange': 'C3'
        }
        color = line_color if line_color is not None else default_colors.get(kind, 'C0')
        ax.plot(x_new, y_new, '-', color=color, linewidth=1.5, alpha=0.9, label=f'Interpolación {kind}', zorder=3)
        ax.scatter(x, y, s=point_size, alpha=0.6, label='Datos originales', zorder=2)
        if y_lo is not None and y_hi is not None:
            ax.set_ylim(y_lo, y_hi)
        ax.legend()
        ax.set_title(f'Gráfica {graph_idx+1} - Interpolación {kind}')
        os.makedirs(output_dir, exist_ok=True)
        output_filename = f"interpolation_graph_{graph_idx+1}_{kind}.png"
        full_output_path = os.path.join(output_dir, output_filename)
        plt.savefig(full_output_path)
        plt.close(fig)
        return full_output_path

    def plot_all_interpolations(self, kind='linear', num_points=200, point_size=6, y_margin_frac=0.05, clip=True, figsize=(12, 8), line_colors=None):

        n = len(self.data_list)
        cols = 3
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        axes = axes.flatten()
        for i in range(len(axes)):
            ax = axes[i]
            if i < n:
                color = None
                if line_colors is not None:
                    try:
                        color = line_colors[i]
                    except Exception:
                        color = None
                self.plot_interpolation(i, kind=kind, num_points=num_points, point_size=point_size, y_margin_frac=y_margin_frac, clip=clip, ax=ax, line_color=color)
            else:
                ax.set_visible(False)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    
    np.random.seed(0)
    data_list = []
    for i in range(5):
        x = np.linspace(0, 10, 10)
        y = np.sin(x) + np.random.normal(scale=0.1, size=x.shape) + i  # Datos ejemplo
        data_list.append((x, y))

    interpolador = Interpolator(data_list)

   
    interpolador.plot_interpolation(0, kind='linear')
    interpolador.plot_interpolation(0, kind='cubic')
    interpolador.plot_interpolation(0, kind='lagrange')
