from django.urls import path
from . import views

urlpatterns = [
    path('planograma/analizar-imagen/', views.planograma_analizar_imagen, name='planograma_analizar_imagen'),
] 