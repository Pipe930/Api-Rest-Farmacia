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