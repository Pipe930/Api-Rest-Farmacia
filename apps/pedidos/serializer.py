from rest_framework import serializers
from .models import Proveedor, Bodeguero, GuiaDespacho, ProductoDespacho, Pedido
    
class ProveedorSerializer(serializers.ModelSerializer):

    class Meta:

        model = Proveedor
        fields = "__all__"

    def create(self, validated_data):

        proveedor = Proveedor.objects.create(**validated_data)

        return proveedor
    
class BodegueroSerializer(serializers.ModelSerializer):

    class Meta:

        model = Bodeguero
        fields = "__all__"

    def create(self, validated_data):

        bodeguero = Bodeguero.objects.create(**validated_data)

        return bodeguero
    
class PedidoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Pedido
        fields = ["fecha_emicion", "estado", "destino", "productos", "cantidad_total", "id_bodeguero", "id_proveedor"]

class CrearPedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ["id_bodeguero", "id_proveedor", "destino", "productos"] 

    def create(self, validated_data):

        pedido = Pedido.objects.create(**validated_data)

        return pedido
    
class ActualizarEstadoPedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ["estado"]
    
    def update(self, instance, validated_data):

        instance.estado = validated_data.get("estado", instance.estado)

        instance.save()

        return instance
    
class GuiaDespachoSerializer(serializers.ModelSerializer):

    class Meta:

        model = GuiaDespacho
        fields = "__all__"

    def create(self, validated_data):

        guiadespacho = GuiaDespacho.objects.create(**validated_data)

        return guiadespacho