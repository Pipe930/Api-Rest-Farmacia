from apps.productos.models import Producto
from .models import Items

class DescuentoStock():

    def get_objeto(self, id_producto:int):

        try:
            producto = Producto.objects.get(id_producto=id_producto)
        except Producto.DoesNotExist:
            return 0

        return producto

    def descontar_stock_producto(self, id_carrito:int):

        items_usuario = Items.objects.filter(id_carrito=id_carrito)

        for items in items_usuario:

            cantidad_item = items.cantidad
            producto_stock = items.producto.stock

            nuevo_stock = producto_stock - cantidad_item

            producto = self.get_objeto(items.producto.id_producto)

            producto.stock = nuevo_stock

            producto.save()

    def limpiar_carrito(self, id_carrito:int):

        items_usuario = Items.objects.filter(id_carrito=id_carrito)

        for items in items_usuario:
            items.delete()
