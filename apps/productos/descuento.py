def descuento(precio_producto, descuento) -> int:

    descuento_decimal = descuento / 100
    percio_descuento = precio_producto * descuento_decimal

    resultado = precio_producto - percio_descuento

    return resultado
