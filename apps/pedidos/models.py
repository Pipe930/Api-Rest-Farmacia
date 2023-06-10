from django.db import models
from django.db.models.signals import pre_save
from apps.sucursales.models import Sucursal
from apps.productos.models import Bodega, Producto
from uuid import uuid4

class Proveedor(models.Model):

    id_proveedor = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    telefono = models.PositiveIntegerField(unique=True)

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
    run = models.PositiveIntegerField(unique=True)
    dv = models.CharField(max_length=1)
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
    code = models.UUIDField(default=uuid4, unique=True)
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
    id_guia_despacho = models.ForeignKey(GuiaDespacho, on_delete=models.CASCADE, related_name="productos")

    class Meta:

        db_table = 'producto_despacho'

# Clase Factura

class Factura(models.Model):

    id_factura = models.BigAutoField(primary_key=True)
    code = models.UUIDField(unique=True, default=uuid4)
    fecha_emicion = models.DateField(auto_now_add=True)
    productos = models.JSONField()
    precio_total = models.PositiveIntegerField()
    productos_total = models.PositiveIntegerField()
    id_bodeguero = models.ForeignKey(Bodeguero, on_delete=models.CASCADE)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    class Meta:

        db_table = 'factura'
        verbose_name = 'factura'
        verbose_name_plural = 'facturas'

    def __str__(self):
        return str(self.code)
    
# Funcion para calcular la cantidad de productos totales de la factura
def set_cantidad_total(sender, instance, *args, **kwargs):

    productos = instance.productos

    cantidad_total = 0

    for producto in productos["productos"]:
        cantidad_total += producto["cantidad"]

    instance.cantidad_total = cantidad_total

pre_save.connect(set_cantidad_total, sender = Factura)
    

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
    destino = models.CharField(max_length=255)
    id_bodeguero = models.ForeignKey(Bodeguero, on_delete=models.CASCADE)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    class Meta:

        db_table = 'pedido'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'

    def __str__(self) -> str:
        return str(self.id_bodeguero)