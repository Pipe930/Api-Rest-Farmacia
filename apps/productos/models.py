from django.db import models

class Oferta(models.Model):

    id_oferta = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_termino = models.DateField()
    descuento = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return self.nombre
    
    class Meta:

        db_table = "oferta"
        verbose_name = "oferta"
        verbose_name_plural = "ofertas"

class Categoria(models.Model):

    id_categoria = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.nombre
    
    class Meta:

        db_table = "categoria"
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

class Producto(models.Model):

    id_producto = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(default="(Sin Descripcion)", blank=True, null=True)
    id_oferta = models.ForeignKey(Oferta, on_delete=models.SET_NULL, blank=True, null=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nombre
    
    class Meta:

        db_table = "producto"
        verbose_name = "producto"
        verbose_name_plural = "productos"


class Bodega(models.Model):

    id_bodega = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    direccion = models.CharField(max_length=255)
    temperatura = models.PositiveSmallIntegerField()
    capacidad = models.PositiveIntegerField()
    capacidad_ocupada = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.nombre
    
    class Meta:

        db_table = "bodega"
        verbose_name = "bodega"
        verbose_name_plural = "bodegas"

class DetalleBodega(models.Model):

    id_detalle_bodega = models.BigAutoField(primary_key=True)
    stock = models.PositiveIntegerField()
    id_bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:

        db_table = "detallebodega"