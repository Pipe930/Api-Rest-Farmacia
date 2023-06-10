from rest_framework import serializers
from .models import Proveedor, Bodeguero, GuiaDespacho, ProductoDespacho, Pedido, Factura
# from apps.usuarios.models import Usuario
# from farmacia.permission import generar_username
    
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
        fields = ["nombre", "apellido", "correo", "telefono", "run", "dv", "id_bodega"]

    def create(self, validated_data):

        bodeguero = Bodeguero.objects.create(**validated_data)

        # username = generar_username(bodeguero.nombre, bodeguero.apellido)

        # password = f"{bodeguero.nombre[0].upper()}{str(bodeguero.run)}{bodeguero.dv}"
        # print(password)

        # Usuario.objects.create_grocer(
        #     username = username,
        #     nombre = bodeguero.nombre,
        #     apellido = bodeguero.apellido,
        #     correo = bodeguero.correo,
        #     password = password
        # )

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
    
class ProductosGuiaDespachoSerializer(serializers.ModelSerializer):

    id_producto = serializers.StringRelatedField()

    class Meta:

        model = ProductoDespacho
        fields = ["cantidad", "id_producto"]

class CrearGuiaDespachoSerializer(serializers.ModelSerializer):

    productos = ProductosGuiaDespachoSerializer(many=True)

    class Meta:

        model = GuiaDespacho
        fields = ["destino", "id_sucursal", "id_bodeguero", "productos"]

    def create(self, validated_data):

        productos_despacho = validated_data.pop("productos")

        guia_despacho = GuiaDespacho.objects.create(**validated_data)

        for diccionario in productos_despacho:

            ProductoDespacho.objects.create(
                cantidad = diccionario["cantidad"],
                id_producto = diccionario["id_producto"],
                id_guia_despacho = guia_despacho
            )

        return guia_despacho
    
class ActualizarEstadoGuiaDespachoSerializer(serializers.ModelSerializer):

    class Meta:

        model = GuiaDespacho
        fields = ["estado"]

    def update(self, instance, validated_data):

        instance.estado = validated_data.get("estado", instance.estado)

        instance.save()

        return instance

class GuiaDespachoSerializer(serializers.ModelSerializer):

    productos = ProductosGuiaDespachoSerializer(many=True)

    class Meta:

        model = GuiaDespacho
        fields = ["activo", "fecha_emicion", "estado", "destino", "productos", "id_sucursal", "id_bodeguero"]

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