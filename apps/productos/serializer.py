from rest_framework import serializers
from .models import Producto, Categoria, Oferta, DetalleBodega, Bodega
from .descuento import discount

class ProductoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Producto
        fields = ["id_producto", "nombre", "stock", "precio", "disponible", "descripcion", "id_oferta"]

    # precio = serializers.SerializerMethodField(method_name="precio_descuento")

    def create(self, validated_data):

        producto = Producto.objects.create(**validated_data)

        return producto
    
    def update(self, instance, validated_data):

        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.precio = validated_data.get("precio", instance.precio)
        instance.stock = validated_data.get("stock", instance.stock)
        instance.disponible = validated_data.get("disponible", instance.disponible)
        instance.descripcion = validated_data.get("descripcion", instance.descripcion)
        instance.id_oferta = validated_data.get("id_oferta", instance.id_oferta)

        instance.save()

        return instance
    
    def precio_descuento(self, producto: Producto):

        if producto.id_oferta is not None:

            precio_final = discount(producto.precio, producto.id_oferta.descuento)

            return precio_final

        return producto.precio
    
class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Categoria
        fields = "__all__"

    def create(self, validated_data):

        categoria = Categoria.objects.create(**validated_data)

        return categoria
    
    def update(self, instance, validated_data):

        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.id_producto = validated_data.get("id_producto", instance.id_producto)

        instance.save()

        return instance
    
class OfertaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Oferta
        fields = ["id_oferta", "nombre", "descuento"]

    def create(self, validated_data):

        oferta = Oferta.objects.create(**validated_data)

        return oferta
    
    def update(self, instance, validated_data):

        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.fecha_termino = validated_data.get("fecha_termino", instance.fecha_termino)
        instance.descuento = validated_data.get("descuento", instance.descuento)

        instance.save()

        return instance
    
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
    
    def update(self, instance, validated_data):

        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.direccion = validated_data.get("direccion", instance.direccion)
        instance.temperatura = validated_data.get("temperatura", instance.temperatura)
        instance.capacidad = validated_data.get("capacidad", instance.capacidad)

        instance.save()

        return instance 