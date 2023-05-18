from .models import Carrito

# Method calculate cart total
def cart_total(id_carrito):

    carrito = Carrito.objects.get(id_carrito=int(id_carrito))

    items = carrito.items.all()
    total = sum([item.cantidad * item.producto.precio for item in items])

    carrito.total = total
    carrito.save()

# Method calculate total price
def calculate_total_price(items) -> int:

    precio_total = 0

    for item in items:

        if item.producto.id_oferta is not None:

            descuento = item.producto.id_oferta.descuento
            precio_producto = item.producto.precio

            descuento_decimal = descuento / 100
            precio_descuento = precio_producto * descuento_decimal

            precio = precio_producto - precio_descuento

        precio = item.producto.precio

        precio_total += item.quantity * precio

    return precio_total