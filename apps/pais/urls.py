from django.urls import path
from . import views

# Urls de las vistas de regiones
urlsRegiones = [
    path("", views.ListarRegionesView.as_view())
]

# Urls de las vistas de provincias
urlsProvincias = [
    path("", views.ListarProvinciasView.as_view()),
    path("created", views.CrearProvinciaView.as_view()),
    path("region/<int:id>", views.ListarProvinciasFilterRegionView.as_view())
]

# Urls de las vistas de comunas
urlsComunas = [
    path("", views.ListarComunasView.as_view()),
    path("created", views.CrearComunaView.as_view()),
    path("provincia/<int:id>", views.ListarComunasFilterProvinciasView.as_view())
]