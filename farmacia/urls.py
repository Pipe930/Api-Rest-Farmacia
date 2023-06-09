
from django.contrib import admin
from django.urls import path, include

from apps.productos.urls import urlsProductos, urlsCategorias, urlsOfertas, urlsBodegas, urlsStockBodega, urlsSoapProductos
from apps.sucursales.urls import urlsSucursales, urlsEmpleados, urlsCargos, urlsDetalleSucursal
from apps.usuarios.urls import urlsUsuarios
from apps.ventas.urls import urlsCompras, urlsCarritos, urlsPedidosCliente, urlsTransbank
from apps.pais.urls import urlsComunas, urlsProvincias, urlsRegiones
from apps.pedidos.urls import urlsBodeguero, urlsProveedor, urlsPedido, urlsFactura, urlsGuiaDespacho

urlpatterns = [
    path('admin/', admin.site.urls),
    path("productos/", include(urlsProductos)),
    path("categorias/", include(urlsCategorias)),
    path("ofertas/", include(urlsOfertas)),
    path("regiones/", include(urlsRegiones)),
    path("provincias/", include(urlsProvincias)),
    path("comunas/", include(urlsComunas)),
    path("sucursales/", include(urlsSucursales)),
    path("detalle-sucursal/", include(urlsDetalleSucursal)),
    path("empleados/", include(urlsEmpleados)),
    path("usuario/", include(urlsUsuarios)),
    path("carrito/", include(urlsCarritos)),
    path("compras/", include(urlsCompras)),
    path("pedidos-cliente/", include(urlsPedidosCliente)),
    path("bodegas/", include(urlsBodegas)),
    path("cargos/", include(urlsCargos)),
    path("stock-bodegas/", include(urlsStockBodega)),
    path("soap/", include(urlsSoapProductos)),
    path("bodegueros/", include(urlsBodeguero)),
    path("proveedores/", include(urlsProveedor)),
    path("pedidos/", include(urlsPedido)),
    path("facturas/", include(urlsFactura)),
    path("guias-despacho/", include(urlsGuiaDespacho)),
    path("transbank/", include(urlsTransbank))
]

handler404 = ""
handler500 = ""