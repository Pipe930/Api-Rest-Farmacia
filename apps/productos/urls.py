from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlsProductos = [
    path("", views.ListaProductosView.as_view()),
    path("producto/<int:id>", views.DetalleProductoView.as_view())
]