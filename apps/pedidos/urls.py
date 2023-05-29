from django.urls import path
from . import views

urlsBodeguero = [
    path("", views.ListarBodeguerosView.as_view())
]