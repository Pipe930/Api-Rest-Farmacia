from rest_framework import serializers
from .models import PedidoCliente, Compra, Carrito, Items
from apps.productos.models import Producto
from django.http import Http404
from apps.productos.descuento import descuento
from .total_carrito import calcular_precio_total, carrito_total, calcular_total_productos, calcular_total_cantidad 
from .descontar_stock import DescuentoStock

class PedidoClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = PedidoCliente
        fields = "__all__"

    def create(self, validated_data):

        pedido_cliente = PedidoCliente.objects.create(**validated_data)

        return pedido_cliente

class CompraSerializer(serializers.ModelSerializer):

    class Meta:

        model = Compra
        fields = "__all__"

    def create(self, validated_data):

        id_carrito = validated_data["id_carrito"]

        descuento_stock = DescuentoStock()

        descuento_stock.descontar_stock_producto(id_carrito)

        compra = Compra.objects.create(**validated_data)

        descuento_stock.limpiar_carrito(id_carrito)

        carrito_total(id_carrito)
        calcular_total_cantidad(id_carrito)
        calcular_total_productos(id_carrito)

        return compra

class CancelarCompraSerializer(serializers.ModelSerializer):

    estado = serializers.BooleanField()

    class Meta:

        model = Compra
        fields = ["estado"]

    def update(self, instance, validated_data):

        instance.estado = validated_data.get('estado', instance.estado)

        instance.save()

        return instance

class UnProductoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Producto
        fields = ["id_producto", "nombre", "precio"]

class ItemsSerializer(serializers.ModelSerializer):

    producto = UnProductoSerializer(many=False)
    precio = serializers.SerializerMethodField(method_name="total")

    class Meta:

        model = Items
        fields = ["id_carrito", "producto", "cantidad", "precio"]

    def total(self, item: Items):

        if item.producto.id_oferta is not None:

            precio = descuento(item.producto.precio, item.producto.id_oferta.descuento)
        else:

            precio = item.producto.precio

        resultado = item.cantidad * precio

        item.precio = resultado
        item.save()

        return resultado

class CarritoSerializer(serializers.ModelSerializer):

    items = ItemsSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name="precio_total")
    cantidad_total = serializers.SerializerMethodField(method_name="calcular_cantidad_total")
    productos_total = serializers.SerializerMethodField(method_name="calcular_productos_total")

    class Meta:

        model = Carrito
        fields = ["id_carrito", "items", "total", "id_usuario", "cantidad_total", "productos_total"]

    def precio_total(self, carrito: Carrito):

        items = carrito.items.all()
        total = calcular_precio_total(items)

        carrito.total = total
        carrito.save()

        return total
    
    def calcular_cantidad_total(self, carrito: Carrito):

        cantidad_total = calcular_total_cantidad(carrito)

        return cantidad_total

    def calcular_productos_total(self, carrito: Carrito):

        cantidad_productos = calcular_total_productos(carrito)

        return cantidad_productos

    def create(self, validated_data):

        carrito = Carrito.objects.create(**validated_data)

        return carrito

class AgregarCarritoItemSerializer(serializers.ModelSerializer):

    class Meta:

        model = Items
        fields = ["producto", "cantidad", "id_carrito"]

    def save(self, **kwargs):

        producto = self.validated_data["producto"]
        cantidad = self.validated_data["cantidad"]
        id_carrito = self.validated_data["id_carrito"]

        try:

            cartitem = Items.objects.get(producto=producto, id_carrito=id_carrito)

            if producto.stock > cartitem.cantidad:

                cartitem.cantidad += cantidad
                cartitem.precio = cartitem.cantidad * cartitem.producto.precio

                cartitem.save()

                carrito_total(id_carrito)
                calcular_total_cantidad(id_carrito)
                calcular_total_productos(id_carrito)

                self.instance = cartitem

        except Items.DoesNotExist:

            if producto.stock > cantidad:

                nuevoPrecio = producto.precio * cantidad

                self.instance = Items.objects.create(
                    producto=producto,
                    id_carrito=id_carrito,
                    cantidad=cantidad,
                    precio=nuevoPrecio
                    )

                carrito_total(id_carrito)
                calcular_total_cantidad(id_carrito)
                calcular_total_productos(id_carrito)

        return self.instance
    
class RestarCarritoItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = ["producto", "id_carrito"]

    def save(self, **kwargs):
        try:
            
            producto = self.validated_data["producto"]
            id_carrito = self.validated_data["id_carrito"]

        except KeyError:
            raise Http404

        try:
            cartitem = Items.objects.get(producto=producto, id_carrito=id_carrito)
        except Items.DoesNotExist:
            raise Http404

        if cartitem.cantidad == 1:

            cartitem.delete()

            carrito_total(cartitem.id_carrito)
            calcular_total_cantidad(id_carrito)
            calcular_total_productos(id_carrito)

            return self.instance

        cartitem.cantidad -= 1
        cartitem.precio = cartitem.cantidad * cartitem.producto.precio
        cartitem.save()

        carrito_total(cartitem.id_carrito)
        calcular_total_cantidad(id_carrito)
        calcular_total_productos(id_carrito)

        return self.instance