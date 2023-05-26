from django.urls import path
from . import views

urlsRegiones = [
    path("", views.ListarRegionesView.as_view())
]

urlsProvincias = [
    path("", views.ListarProvinciasView.as_view()),
    path("created", views.CrearProvinciaView.as_view()),
    path("region/<int:id>", views.ListarProvinciasFilterRegionView.as_view())
]

urlsComunas = [
    path("", views.ListarComunasView.as_view()),
    path("created", views.CrearComunaView.as_view()),
    path("provincia/<int:id>", views.ListarComunasFilterProvinciasView.as_view())
]