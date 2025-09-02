from django.urls import path
from Apps.DataVisualization.views import randomGraph

urlpatterns = [
    path("randomGraph/", randomGraph, name="randomGraph"),
]
