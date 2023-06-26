from django.urls import path
from . import views

# Urls Bodegueros
urlsBodeguero = [
    path("", views.ListarBodeguerosView.as_view()),
    path("created", views.CrearBodegueroView.as_view()),
    path("bodeguero/<int:id>", views.DetalleBodegueroView.as_view())
]

# Urls Proveedores
urlsProveedor = [
    path("", views.ListarProveedoresView.as_view()),
    path("created", views.CrearProveedorView.as_view()),
    path("proveedor/<int:id>", views.DetalleProveedorView.as_view())
]

# Urls Pedidos
urlsPedido = [
    path("", views.ListarPedidosView.as_view()),
    path("factura/<int:id>", views.ListarPedidosFacturaView.as_view()),
    path("update/estado/<int:id>", views.ActualizarEstadoPedidoView.as_view()),
    path("pedido/<int:id>", views.DetallePedidoView.as_view())
]

# Urls Facturas
urlsFactura = [
    path("", views.ListarFacturasView.as_view()),
    path("proveedor/<int:id>", views.FacturasProveedorView.as_view()),
    path("created", views.CrearFacturaView.as_view()),
    path("factura/<int:id>", views.DetalleFacturaView.as_view())
]

# Urls Guias Despacho
urlsGuiaDespacho = [
    path("", views.ListarGuiaDespachoView.as_view()),
    path("created", views.CrearGuiaDespachoView.as_view()),
    path("sucursal/<int:id>", views.ListarGuiaDespachoSucursalView.as_view()),
    path("guia-despacho/<int:id>", views.DetalleGuiaDespachoView.as_view()),
    path("update/<int:id>", views.ActualizarEstadoGuiaDespachoView.as_view())
]