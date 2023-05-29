from rest_framework import serializers
from .models import Producto, Categoria, Oferta, DetalleBodega, Bodega
from .descuento import descuento
from rest_framework import status

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
    
class ActualizarOfertaProductoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Producto
        fields = ["id_oferta"]

    def update(self, instance, validated_data):

        instance.id_oferta = validated_data.get("id_oferta", instance.id_oferta)

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
    
class StockBodegaSerializer(serializers.ModelSerializer):

    id_producto = serializers.StringRelatedField()

    class Meta:

        model = DetalleBodega
        fields = "__all__"
    
class CrearStockBodegaSerializer(serializers.ModelSerializer):

    class Meta:

        model = DetalleBodega
        fields = "__all__"

    def save(self, **kwargs):

        id_bodega = self.data["id_bodega"]
        stock = self.validated_data["stock"]
        id_producto = self.validated_data["id_producto"]

        bodega = Bodega.objects.get(id_bodega=id_bodega)
        
        try:
            producto = DetalleBodega.objects.get(id_producto=id_producto, id_bodega=id_bodega)

            sumar_stock = producto.stock + stock

            producto.stock = sumar_stock

            stock_bodega = bodega.capacidad_ocupada

            nuevo_stock = stock + stock_bodega

            if bodega.capacidad > nuevo_stock:

                bodega.capacidad_ocupada = nuevo_stock

                bodega.save()
                producto.save()

                self.instance = producto

                return self.instance

            raise serializers.ValidationError({"status": "Conflict", "message": "La capacidad ocupa de la bodega supera a la capacidad maxima de la bodega"}, status.HTTP_409_CONFLICT)
        
        except DetalleBodega.DoesNotExist:

            stock_bodega = bodega.capacidad_ocupada

            nuevo_stock = stock + stock_bodega

            if bodega.capacidad > nuevo_stock:

                bodega.capacidad_ocupada = nuevo_stock

                bodega.save()

                self.instance = DetalleBodega.objects.create(**self.validated_data)

                return self.instance
            
            raise serializers.ValidationError({"status": "Conflict", "message": "La capacidad ocupa de la bodega supera a la capacidad maxima de la bodega"}, status.HTTP_409_CONFLICT)

    
class BodegaSerialzer(serializers.ModelSerializer):

    class Meta:

        model = Bodega
        fields = "__all__"

    def create(self, validated_data):

        bodega = Bodega.objects.create(**validated_data)

        return bodega
