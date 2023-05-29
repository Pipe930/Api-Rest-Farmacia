from rest_framework import serializers
from .models import Proveedor, Bodeguero, GuiaDespacho, ProductoDespacho, ProductoPedido, Pedido
    
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
        fields = "__all__"

    def create(self, validated_data):

        pedido = Pedido.objects.create(**validated_data)

        return pedido
    
class GuiaDespachoSerializer(serializers.ModelSerializer):

    class Meta:

        model = GuiaDespacho
        fields = "__all__"

    def create(self, validated_data):

        guiadespacho = GuiaDespacho.objects.create(**validated_data)

        return guiadespacho