from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .soap_view import crud_producto

urlsProductos = [
    path("", views.ListarProductosView.as_view()),
    path("created", views.CrearProductoView.as_view()),
    path("categoria/<int:id>", views.ListarProductoFilterCategoriaView.as_view()),
    path("oferta", views.ListarProductosOfertaView.as_view()),
    path("producto/<int:id>", views.DetalleProductoView.as_view()),
    path("update-stock/<int:id>", views.ActualizarStockProductoView.as_view()),
    path("producto", views.BuscarProductoView.as_view()),
    path("update-oferta/<int:id>", views.ActualizarOfertaProductoView.as_view())
]

urlsSoapProductos = [
    path("producto/", crud_producto)
]

urlsStockBodega = [
    path("created", views.CrearProductosBodegaView.as_view()),
    path("bodega/<int:id>", views.ListarStockProductosFilterBodegaView.as_view()),
    path("producto/<int:id>", views.ListarStockBodegasFilterProductoView.as_view())
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