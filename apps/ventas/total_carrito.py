from .models import Carrito

def carrito_total(id_carrito):

    carrito = Carrito.objects.get(id_carrito=int(id_carrito.id_carrito))

    items = carrito.items.all()

    total = sum([item.cantidad * item.producto.precio for item in items])

    carrito.total = total
    carrito.save()

def calcular_precio_total(items) -> int:

    precio_total = 0

    for item in items:

        if item.producto.id_oferta is not None:

            descuento = item.producto.id_oferta.descuento
            precio_producto = item.producto.precio

            descuento_decimal = descuento / 100
            precio_descuento = precio_producto * descuento_decimal

            precio = precio_producto - precio_descuento

        else:

            precio = item.producto.precio

        precio_total += item.cantidad * precio

    return precio_total


def calcular_total_cantidad(id_carrito):

    carrito = Carrito.objects.get(id_carrito=int(id_carrito.id_carrito))

    items = carrito.items.all()

    cantidad_total = 0

    for item in items:
        cantidad_total += item.cantidad

    carrito.cantidad_total = cantidad_total
    carrito.save()

    return cantidad_total

def calcular_total_productos(id_carrito):

    carrito = Carrito.objects.get(id_carrito=int(id_carrito.id_carrito))

    items = carrito.items.all()

    cantidad_productos = 0
    for item in items:
        cantidad_productos += 1

    carrito.productos_total = cantidad_productos
    carrito.save()

    return cantidad_productos