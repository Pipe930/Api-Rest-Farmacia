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

urlsSucursales = [
    path("", views.ListarSucursalesView.as_view()),
    path("sucursal/<int:id>", views.DetalleSucursalView.as_view())
]

urlsEmpleados = [
    path("", views.ListarEmpleadosView.as_view()),
    path("sucursal/<int:id>", views.DetalleEmpleadoView.as_view())
]