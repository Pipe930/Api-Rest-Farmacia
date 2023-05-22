from typing import Tuple
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Class to create users
class UserManager(BaseUserManager):

    # Method of creating a new user
    def _create_user(self, username, correo, nombre, apellido, password, is_staff, is_superuser, **extra_fields):

        #The user model is instantiated
        user = self.model(
            username = username,
            correo = self.normalize_email(correo),
            nombre = nombre,
            apellido = apellido,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )

        user.set_password(password) # Password is encrypted
        user.save(using = self.db) # The new user is saved in the database

        return user

    # Method of creating a user
    def create_user(self, username, correo, nombre, apellido, password=None, **extra_fields):
        return self._create_user(username, correo, nombre, apellido, password, False, False, **extra_fields)

    # Method of creating a superuser
    def create_superuser(self, username, correo, nombre, apellido, password=None, **extra_fields):
        return self._create_user(username, correo, nombre, apellido, password, True, True, **extra_fields)

# User Model
class Usuario(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=60, unique=True)
    correo = models.EmailField("Correo", max_length=255, unique=True)
    nombre = models.CharField("Nombre", max_length=20, blank=True, null=True, default="(Sin Nombre)")
    apellido = models.CharField("Apellido", max_length=20, blank=True, null=True, default="(Sin Apellido)")
    date_joined = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        db_table = "usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nombre", "apellido", "correo"]

    def natural_key(self) -> Tuple[str]:
        return (self.username,)

    def __str__(self) -> str:
        return self.username