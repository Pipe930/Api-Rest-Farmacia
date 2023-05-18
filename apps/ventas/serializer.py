from rest_framework import serializers
from .models import Orden, Compra, Carrito, Items
from apps.productos.models import Producto
from django.http import Http404
from apps.productos.descuento import discount
from .total_carrito import calculate_total_price, cart_total
from .descontar_stock import DescuentoStock

class OrdenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orden
        fields = "__all__"

    def create(self, validated_data):

        orden = Orden.objects.create(**validated_data)

        return orden

class CompraSerializer(serializers.ModelSerializer):

    class Meta:

        model = Compra
        fields = "__all__"

    def create(self, validated_data):

        id_carrito = validated_data["id_carrito"]

        descuento_stock = DescuentoStock()

        descuento_stock.discount_stock_product(id_carrito)

        compra = Compra.objects.create(**validated_data)

        descuento_stock.clean_cart(id_carrito)

        cart_total(id_carrito)

        return compra

class CancelarCompraSerializer(serializers.ModelSerializer):

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
        fields = ["id_producto", "nombre", "precio", "stock"]

class ItemsSerializer(serializers.ModelSerializer):

    producto = UnProductoSerializer(many=False)
    precio = serializers.SerializerMethodField(method_name="total")

    class Meta:

        model = Items
        fields = ["id_carrito", "producto", "cantidad", "precio"]

    def total(self, item: Items):

        if item.producto.id_oferta is not None:

            precio = discount(item.producto.precio, item.producto.id_oferta.descuento)

        precio = item.producto.precio

        resultado = item.cantidad * precio
        return resultado

class CarritoSerializer(serializers.ModelSerializer):

    items = ItemsSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:

        model = Carrito
        fields = ("id_carrito", "items", "total", "id_usuario")

    def main_total(self, carrtio: Carrito):

        items = carrtio.items.all()
        total = calculate_total_price(items)
        return total

    def create(self, validated_data):

        carrtio = Carrito.objects.create(**validated_data)
        return carrtio

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

            if cartitem.producto.stock > cartitem.cantidad:

                cartitem.cantidad += cantidad
                cartitem.precio = cartitem.cantidad * cartitem.producto.precio

                cartitem.save()

                cart_total(id_carrito)

                self.instance = cartitem

        except Items.DoesNotExist:

            producto2 = Producto.objects.get(id_producto=int(producto.id_producto))

            if producto2.stock > cantidad:

                nuevoPrecio = producto2.precio * cantidad

                self.instance = Items.objects.create(
                    producto=producto,
                    id_carrito=id_carrito,
                    cantidad=cantidad,
                    precio=nuevoPrecio
                    )

                cart_total(id_carrito)

        return self.instance

# Substract Cart serializer
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

        cartitem.cantidad -= 1
        cartitem.precio = cartitem.cantidad * cartitem.producto.precio
        cartitem.save()

        cart_total(cartitem.id_carrito)

        return self.instance