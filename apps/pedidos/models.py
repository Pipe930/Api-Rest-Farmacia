from django.db import models
from apps.sucursales.models import Sucursal
from apps.productos.models import Bodega, Producto

class Proveedor(models.Model):

    id_proveedor = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    telefono = models.PositiveIntegerField()

    class Meta:

        db_table = 'proveedor'
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'

    def __str__(self) -> str:
        return "{} {}".format(self.nombre, self.apellido)


class Bodeguero(models.Model):

    id_bodeguero = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    telefono = models.PositiveIntegerField()
    id_bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)

    class Meta:

        db_table = 'bodeguero'
        verbose_name = 'bodeguero'
        verbose_name_plural = 'bodegueros'

    def __str__(self) -> str:
        return "{} {}".format(self.nombre, self.apellido)

CHOICES_GUIA_DESPACHO = [
    ("En Preparacion", "En Preparacion"),
    ("En Reparto", "En Reparto"),
    ("En Envio", "En Envio"),
    ("Entregado", "Entregado")
]

class GuiaDespacho(models.Model):

    id_guia_despacho = models.BigAutoField(primary_key=True)
    activo = models.BooleanField(default=True)
    fecha_emicion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=40, choices=CHOICES_GUIA_DESPACHO, default="En Preparacion")
    destino = models.CharField(max_length=255)
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    id_bodeguero = models.ForeignKey(Bodeguero, on_delete=models.CASCADE)

    class Meta:

        db_table = 'guia_despacho'
        verbose_name = 'guia_despacho'
        verbose_name_plural = 'guia_despachos'

    def __str__(self) -> str:
        return str(self.id_bodeguero)
    
class ProductoDespacho(models.Model):

    id_producto_despacho = models.BigAutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_guia_despacho = models.ForeignKey(GuiaDespacho, on_delete=models.CASCADE)

    class Meta:

        db_table = 'producto_despacho'

CHOICES_PEDIDO = [
    ("En Preparacion", "En Preparacion"),
    ("En Reparto", "En Reparto"),
    ("En Envio", "En Envio"),
    ("En Revicion", "En Revicion"),
    ("Almacenado", "Almacenado")
]

class Pedido(models.Model):

    id_pedido = models.BigAutoField(primary_key=True)
    fecha_emicion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=40, choices=CHOICES_PEDIDO, default="En Preparacion")
    id_bodeguero = models.ForeignKey(Bodeguero, on_delete=models.CASCADE)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    class Meta:

        db_table = 'pedido'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'

    def __str__(self) -> str:
        return str(self.id_bodeguero)
    

class ProductoPedido(models.Model):

    id_producto_pedido = models.BigAutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:

        db_table = 'producto_pedido'
