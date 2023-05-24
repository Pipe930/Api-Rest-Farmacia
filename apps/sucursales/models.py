from django.db import models
from apps.productos.models import Producto

class Region(models.Model):

    id_region = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    sigla = models.CharField(max_length=8, blank=True, null=True)

    class Meta:

        db_table = 'region'
        verbose_name = 'region'
        verbose_name_plural = 'regiones'

    def __str__(self) -> str:
        return self.nombre

class Provincia(models.Model):

    id_provincia = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    id_region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:

        db_table = 'provincia'
        verbose_name = 'provincia'
        verbose_name_plural = 'provincias'

    def __str__(self) -> str:
        return self.nombre

class Comuna(models.Model):

    id_comuna = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    id_provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    class Meta:

        db_table = 'comuna'
        verbose_name = 'comuna'
        verbose_name_plural = 'comunas'

    def __str__(self) -> str:
        return self.nombre

class Sucursal(models.Model):

    id_sucursal = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=255)
    razon_social = models.CharField(max_length=100)
    id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    class Meta:

        db_table = 'sucursal'
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'

    def __str__(self) -> str:
        return self.nombre
    
class Cargo(models.Model):

    id_cargo = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=40)

    class Meta:

        db_table = 'cargo'
        verbose_name = 'cargo'
        verbose_name_plural = 'cargos'

    def __str__(self) -> str:
        return self.nombre
    
class Empleado(models.Model):

    id_empleado = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    run = models.PositiveIntegerField(unique=True)
    dv = models.CharField(max_length=1)
    correo = models.EmailField(unique=True)
    fecha_contrato = models.DateField(auto_now_add=True)
    salario = models.PositiveIntegerField()
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    id_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    class Meta:

        db_table = 'empleado'
        verbose_name = 'empleado'
        verbose_name_plural = 'empleados'

    def __str__(self) -> str:
        return "{} {}".format(self.nombre, self.apellido)
    
class DetalleSucursal(models.Model):

    id_detalle_sucursal = models.BigAutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    id_productos = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    class Meta:

        db_table = 'detallesucursal'