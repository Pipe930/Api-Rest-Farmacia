from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlsProductos = [
    path("", views.ListarProductosView.as_view()),
    path("producto/<int:id>", views.DetalleProductoView.as_view()),
    path("producto", views.BuscarProductoView.as_view())
]

urlsCategorias = [
    path("", views.ListarCategoriasView.as_view()),
    path("categoria/<int:id>", views.DetalleCategoriaView.as_view())
]

urlsOfertas = [
    path("", views.ListarOfertasView.as_view()),
    path("oferta/<int:id>", views.DetalleOfertaView.as_view())
]

urlsBodegas = [
    path("", views.ListarBodegasView.as_view()),
    path("bodega/<int:id>", views.DetalleBodegaView.as_view())
]