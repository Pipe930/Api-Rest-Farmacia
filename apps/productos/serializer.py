from rest_framework import serializers
from .models import Producto, Categoria, Oferta, DetalleBodega, Bodega
from .descuento import descuento

class ProductoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Producto
        fields = "__all__"

    precio = serializers.SerializerMethodField(method_name="precio_descuento")
    
    def precio_descuento(self, producto: Producto):

        if producto.id_oferta is not None:

            precio_final = descuento(producto.precio, producto.id_oferta.descuento)

            return precio_final

        return producto.precio
    
class CrearProductoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Producto
        fields = "__all__"

    def create(self, validated_data):

        producto = Producto.objects.create(**validated_data)

        return producto

class ActualizarProductoStockSerializer(serializers.ModelSerializer):

    class Meta:

        model = Producto
        fields = ["precio", "stock"]

    def update(self, instance, validated_data):

        instance.precio = validated_data.get("precio", instance.precio)
        instance.stock = validated_data.get("stock", instance.stock)

        instance.save()

        return instance
    
class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Categoria
        fields = "__all__"

    def create(self, validated_data):

        categoria = Categoria.objects.create(**validated_data)

        return categoria
    
class OfertaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Oferta
        fields = ["nombre", "estado", "fecha_inicio", "fecha_termino", "descuento"]

    def create(self, validated_data):

        oferta = Oferta.objects.create(**validated_data)

        return oferta
    
class DetalleBodegaSerializer(serializers.ModelSerializer):

    class Meta:

        model = DetalleBodega
        fields = "__all__"

    def create(self, validated_data):

        detalle_bodega = DetalleBodega.objects.create(**validated_data)

        return detalle_bodega
    
    def update(self, instance, validated_data):

        instance.stock = validated_data.get("stock", instance.stock)
        instance.id_producto = validated_data.get("id_producto", instance.id_producto)
        instance.id_bodega = validated_data.get("id_bodega", instance.id_bodega)

        instance.save()

        return instance 
    
class BodegaSerialzer(serializers.ModelSerializer):

    class Meta:

        model = Bodega
        fields = "__all__"

    def create(self, validated_data):

        bodega = Bodega.objects.create(**validated_data)

        return bodega