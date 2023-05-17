
from django.contrib import admin
from django.urls import path, include
from apps.productos.urls import urlsProductos

urlpatterns = [
    path('admin/', admin.site.urls),
    path("productos/", include(urlsProductos)),
]
