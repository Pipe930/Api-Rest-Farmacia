from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlsRegiones = [
    path("", views.ListarRegionesView.as_view())
]

urlsProvincias = [
    path("", views.ListarProvinciasView.as_view())
]

urlsComunas = [
    path("", views.ListarComunasView.as_view())
]