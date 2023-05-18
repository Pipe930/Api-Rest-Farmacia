
from django.contrib import admin
from django.urls import path, include
from apps.productos.urls import urlsProductos, urlsCategorias, urlsOfertas
from apps.sucursales.urls import urlsRegiones, urlsProvincias, urlsComunas, urlsSucursales, urlsEmpleados
from apps.users.urls import urlsUsuarios
from apps.ventas.urls import urlsCompras, urlsCarritos, urlsOrdenes

urlpatterns = [
    path('admin/', admin.site.urls),
    path("productos/", include(urlsProductos)),
    path("categorias/", include(urlsCategorias)),
    path("ofertas/", include(urlsOfertas)),
    path("regiones/", include(urlsRegiones)),
    path("provincias/", include(urlsProvincias)),
    path("comunas/", include(urlsComunas)),
    path("sucursales/", include(urlsSucursales)),
    path("empleados/", include(urlsEmpleados)),
    path("usuario/", include(urlsUsuarios)),
    path("carrito/", include(urlsCarritos)),
    path("compras/", include(urlsCompras)),
    path("pedidos/", include(urlsOrdenes))
]
