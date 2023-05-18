from apps.productos.models import Producto
from .models import Items

# Class Discount Stock
class DescuentoStock():

    # Method Obtain a Object Product
    def get_objeto(self, id_producto:int):

        try:
            producto = Producto.objects.get(id_producto=id_producto)
        except Producto.DoesNotExist:
            return 0

        return producto

    # Method of discounting stock of a product
    def discount_stock_product(self, id_carrito:int):

        # Query to get the items from the user's cart
        items_user = Items.objects.filter(id_carrito=id_carrito)

        for items in items_user:

            cantidad_item = items.quantity
            producto_stock = items.product.stock

            nuevo_stock = producto_stock - cantidad_item

            producto = self.get_objeto(items.producto.id_producto)

            producto.stock = nuevo_stock

            producto.save()

    # Method Clean Cart
    def clean_cart(self, id_carrito:int):

        items_usuario = Items.objects.filter(id_carrito=id_carrito)

        for items in items_usuario:
            items.delete()
