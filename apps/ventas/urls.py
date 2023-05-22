from django.urls import path
from . import views

urlsCarritos = [
    path("usuario/<int:idUser>", views.CarritoUsuarioView.as_view()),
    path("item/agregar", views.AgregarCarritoItemView.as_view()),
    path("item/restar", views.RestarCarritoItemView.as_view()),
    path("limpiar/<int:id>", views.LimpiarCarritoView.as_view())
]

urlsCompras = [
    path("crear", views.CrearCompraView.as_view()),
    path("cancel/<int:id>", views.CancelarCompraView.as_view()),
    path("usuario/<int:id>", views.ListarComprasView.as_view()),
    path("<int:id>", views.DetalleCompraView.as_view()),
]

urlsOrdenes = [
    path("", views.ListarOrdenesView.as_view()),
    path("pedido/<int:id>", views.DetalleOrdenView.as_view()),
    path("crear", views.CrearOrdenView.as_view()),
]
