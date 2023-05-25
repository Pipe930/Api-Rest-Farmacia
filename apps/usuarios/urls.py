from django.urls import path
from . import views

urlsUsuarios = [
    path("register", views.RegisterUserView.as_view()),
    path("auth/login", views.LoginView.as_view()),
    path("auth/logout", views.LogoutView.as_view())
]