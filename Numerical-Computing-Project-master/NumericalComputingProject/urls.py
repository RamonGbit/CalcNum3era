"""
URL configuration for NumericalComputingProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from Apps.DataVisualization import views #para las vistas de la app, n estabaan importadas por alguna razon

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dataVisualization/", include("Apps.DataVisualization.urls")),

    path('api/generate-points/', views.generate_line_points, name='api_generate_points'),
    path('api/create-plot/', views.create_plot_image, name='api_create_plot'),
    path('api/generate-and-plot/', views.generate_and_plot, name='api_generate_and_plot'),

]
