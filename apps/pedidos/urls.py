from django.urls import path
from . import views

urlsBodeguero = [
    path("", views.ListarBodeguerosView.as_view()),
    path("created", views.CrearBodegueroView.as_view())
]

urlsProveedor = [
    path("", views.ListarProveedoresView.as_view()),
    path("created", views.CrearProveedorView.as_view())
]

urlsPedido = [
    path("", views.ListarPedidosView.as_view()),
    path("factura/<int:id>", views.ListarPedidosFacturaView.as_view()),
    path("created", views.CrearPedidoView.as_view()),
    path("update/estado/<int:id>", views.ActualizarEstadoPedidoView.as_view())
]

urlsFactura = [
    path("", views.ListarFacturasView.as_view()),
    path("proveedor/<int:id>", views.FacturasProveedorView.as_view()),
    path("created", views.CrearFacturaView.as_view()),
]