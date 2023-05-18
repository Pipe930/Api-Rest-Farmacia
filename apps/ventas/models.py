from django.db import models
from apps.users.models import Usuario
from apps.productos.models import Producto
from apps.sucursales.models import Comuna, Sucursal
from uuid import uuid4

class Carrito(models.Model):

    id_carrito = models.BigAutoField(primary_key=True)
    creado = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:

        db_table = "carrito"
        verbose_name = "carrito"
        verbose_name_plural = "carritos"

    def __str__(self) -> str:
        return str(self.id_usuario.username)

class Items(models.Model):

    id_items = models.BigAutoField(primary_key=True)
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="products")
    cantidad = models.PositiveSmallIntegerField()
    precio = models.PositiveIntegerField()

    class Meta:

        db_table = "item"
        verbose_name = "item"
        verbose_name_plural = "items"

class Compra(models.Model):

    id_compra = models.BigAutoField(primary_key=True)
    codigo = models.UUIDField(default=uuid4, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    precio_total = models.PositiveIntegerField()
    estado = models.BooleanField(default=True)
    productos = models.JSONField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id_usuario.username)

    class Meta:

        db_table = "compra"
        verbose_name = "compra"
        verbose_name_plural = "compras"

CHOICES_WITHDRAWAL = [
    ("retiro en tienda", "retiro en tienda"),
    ("envio a domicilio", "envio a domicilio")
]

CHOICES_CONDITION = [
    ("en preparacion", "en preparacion"),
    ("en reparto", "en reparto"),
    ("en camino", "en camino"),
    ("entregado", "entregado")
]

class Orden(models.Model):

    id_orden = models.BigAutoField(primary_key=True)
    codigo = models.UUIDField(default=uuid4, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    condicion = models.CharField(max_length=20, choices=CHOICES_CONDITION, default="en preparacion")
    tipo_retiro = models.CharField(max_length=20, choices=CHOICES_WITHDRAWAL)
    direccion = models.CharField(max_length=100)
    num_departamento = models.PositiveSmallIntegerField(blank=True, null=True)
    id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, blank=True, null=True)
    id_compra = models.ForeignKey(Compra, on_delete=models.CASCADE)

    class Meta:

        db_table = 'orden'
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes'

    def __str__(self) -> str:
        return str(self.id_compra)