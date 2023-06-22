from rest_framework import serializers
from .models import Empleado, DetalleSucursal, Sucursal, Cargo
    
class EmpleadoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Empleado
        fields = "__all__"

    def create(self, validated_data):

        empleado = Empleado.objects.create(**validated_data)

        return empleado
    
class ActualizarEmpladoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Empleado
        fields = ["salario", "id_sucursal", "id_cargo"]

    def update(self, instance, validated_data):

        instance.salario = validated_data.get("salario", instance.salario)
        instance.id_sucursal = validated_data.get("id_sucursal", instance.id_sucursal)
        instance.id_cargo = validated_data.get("id_cargo", instance.id_cargo)

        instance.save()

        return instance
    
class SucursalSerializer(serializers.ModelSerializer):

    class Meta:

        model = Sucursal
        fields = "__all__"

    def create(self, validated_data):

        sucursal = Sucursal.objects.create(**validated_data)

        return sucursal
    
class CargoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Cargo
        fields = "__all__"

    def create(self, validated_data):

        cargo = Cargo.objects.create(**validated_data)

        return cargo
    
    def update(self, instance, validated_data):

        instance.nombre = validated_data.get("nombre", instance.nombre)

        instance.save()

        return instance

class CargarProductosSucursalSerializer(serializers.ModelSerializer):

    class Meta:

        model = DetalleSucursal
        fields = ["id_productos", "id_sucursal", "cantidad"]


    def validate(self, attrs):

        if attrs.get("cantidad") == 0:
            raise serializers.ValidationError("La cantidad tiene que ser mayor a 0")

        return attrs

    def save(self, **kwargs):

        id_producto = self.validated_data["id_productos"]
        id_sucursal = self.validated_data["id_sucursal"]
        cantidad = self.validated_data["cantidad"]

        try:

            productos_sucursal = DetalleSucursal.objects.get(id_sucursal_id=id_sucursal, id_productos_id=id_producto)

            productos_sucursal.cantidad += cantidad

            productos_sucursal.save()

            self.instance = productos_sucursal

        except DetalleSucursal.DoesNotExist:

            self.instance = DetalleSucursal.objects.create(**self.validated_data)

        return self.instance
    
class ListarProductosSucursalSerializer(serializers.ModelSerializer):

    id_productos = serializers.StringRelatedField()

    class Meta:

        model = DetalleSucursal
        fields = ["id_sucursal", "id_productos", "cantidad"]