from rest_framework import serializers
from .models import Proveedor, Bodeguero, GuiaDespacho, ProductoDespacho, Pedido, Factura
    
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
        fields = ["fecha_emicion", "estado", "destino", "id_bodeguero", "id_factura"]

class CrearPedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ["id_bodeguero", "id_factura", "destino"] 

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

class CrearGuiaDespachoSerializer(serializers.ModelSerializer):

    class Meta:

        model = GuiaDespacho
        fields = ["destino", "id_sucursal", "id_bodeguero"]

    def create(self, validated_data):

        guia_despacho = GuiaDespacho.objects.create(**validated_data)

        return  guia_despacho

class GuiaDespachoSerializer(serializers.ModelSerializer):

    class Meta:

        model = GuiaDespacho
        fields = ["activo", "fecha_emicion", "estado", "destino", "id_sucursal"]

class FacturaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Factura
        fields = ["activo", "fecha_emicion", "productos", "precio_total", "id_proveedor", "id_bodeguero"]

class CrearFacturaSerialzer(serializers.ModelSerializer):

    class Meta:

        model = Factura
        fields = ["productos", "precio_total", "id_bodeguero", "id_proveedor"]

    def create(self, validated_data):

        factura = Factura.objects.create()

        return factura