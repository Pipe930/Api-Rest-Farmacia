from django.db import models

# Modelo Region
class Region(models.Model):

    # Atributos
    id_region = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=60, unique=True)
    sigla = models.CharField(max_length=8, blank=True, null=True)

    class Meta:

        db_table = 'region'
        verbose_name = 'region'
        verbose_name_plural = 'regiones'

    def __str__(self) -> str:
        return self.nombre

# Modelo Provincia
class Provincia(models.Model):

    id_provincia = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=40, unique=True)
    id_region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:

        db_table = 'provincia'
        verbose_name = 'provincia'
        verbose_name_plural = 'provincias'

    def __str__(self) -> str:
        return self.nombre

# Modelo Comuna
class Comuna(models.Model):

    id_comuna = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=40, unique=True)
    id_provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    class Meta:

        db_table = 'comuna'
        verbose_name = 'comuna'
        verbose_name_plural = 'comunas'

    def __str__(self) -> str:
        return self.nombre
