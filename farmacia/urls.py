
from django.contrib import admin
from django.urls import path, include
from apps.productos.urls import urlsProductos, urlsCategorias, urlsOfertas

urlpatterns = [
    path('admin/', admin.site.urls),
    path("productos/", include(urlsProductos)),
    path("categorias/", include(urlsCategorias)),
    path("ofertas/", include(urlsOfertas)),
]
