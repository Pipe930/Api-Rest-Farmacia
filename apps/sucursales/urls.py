from django.urls import path
from . import views

urlsSucursales = [
    path("", views.ListarSucursalesView.as_view()),
    path("sucursal/<int:id>", views.DetalleSucursalView.as_view())
]

urlsEmpleados = [
    path("", views.ListarEmpleadosView.as_view()),
    path("empleado/<int:id>", views.DetalleEmpleadoView.as_view())
]

urlsCargos = [
    path("", views.ListarCargosView.as_view()),
    path("cargo/<int:id>", views.DetalleCargoView.as_view())
]