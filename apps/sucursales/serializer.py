from rest_framework import serializers
from .models import Region, Provincia, Comuna, Empleado, DetalleSucursal, Sucursal

class RegionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Region
        fields = "__all__"

    def create(self, validated_data):

        region = Region.objects.create(**validated_data)

        return region
    
class ProvinciaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Provincia
        fields = "__all__"

    def create(self, validated_data):

        provincia = Provincia.objects.create(**validated_data)

        return provincia
    
class ComunaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Comuna
        fields = "__all__"

    def create(self, validated_data):

        comuna = Comuna.objects.create(**validated_data)

        return comuna
    
class EmpleadoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Empleado
        fields = "__all__"

    def create(self, validated_data):

        empleado = Empleado.objects.create(**validated_data)

        return empleado
    
    def update(self, instance, validated_data):

        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.apellido = validated_data.get("apellido", instance.apellido)
        instance.run = validated_data.get("run", instance.run)
        instance.dv = validated_data.get("dv", instance.dv)
        instance.correo = validated_data.get("correo", instance.correo)
        instance.salario = validated_data.get("salario", instance.salario)
        instance.id_sucursal = validated_data.get("id_sucursal", instance.id_sucursal)


        instance.save()

        return instance
    
class SucursalSerializer(serializers.ModelSerializer):

    class Meta:

        model = Sucursal
        fields = "__all__"

    def create(self, validated_data):

        sucursal = Sucursal.objects.create(**validated_data)

        return sucursal
    
    def update(self, instance, validated_data):

        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.direccion = validated_data.get("direccion", instance.direccion)
        instance.razon_social = validated_data.get("razon_social", instance.razon_social)
        instance.id_comuna = validated_data.get("id_comuna", instance.id_comuna)

        instance.save()

        return instance