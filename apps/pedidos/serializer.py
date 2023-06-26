from rest_framework import serializers
from .models import Proveedor, Bodeguero, GuiaDespacho, ProductoDespacho, Pedido, Factura
# from apps.usuarios.models import Usuario
# from farmacia.permission import generar_username

# Serializadores
    
# Proveedor Serializer
class ProveedorSerializer(serializers.ModelSerializer):

    class Meta:

        model = Proveedor
        fields = "__all__"

    # Metodo Crear un proveedor
    def create(self, validated_data):

        proveedor = Proveedor.objects.create(**validated_data)

        return proveedor

# Bodeguero Serializer
class BodegueroSerializer(serializers.ModelSerializer):

    class Meta:

        model = Bodeguero
        fields = ["nombre", "apellido", "correo", "telefono", "run", "dv", "id_bodega"]

    # Metodo Crear un bodeguero
    def create(self, validated_data):

        bodeguero = Bodeguero.objects.create(**validated_data)

        # username = generar_username(bodeguero.nombre, bodeguero.apellido)

        # password = f"{bodeguero.nombre[0].upper()}{str(bodeguero.run)}{bodeguero.dv}"
        # print(password)

        # Usuario.objects.create_grocer(
        #     username = username,
        #     nombre = bodeguero.nombre,
        #     apellido = bodeguero.apellido,
        #     correo = bodeguero.correo,
        #     password = password
        # )

        return bodeguero
    
# Pedido Serializer
class PedidoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Pedido
        fields = ["fecha_emicion", "estado", "destino", "id_bodeguero", "id_factura"]

# Crear un pedido serializer
class CrearPedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ["destino"] 

# Actualizar estado de pedido Serializer
class ActualizarEstadoPedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ["estado"]
    
    # Metodo de actualizar campos de un modelo pedido
    def update(self, instance, validated_data):

        instance.estado = validated_data.get("estado", instance.estado)

        instance.save()

        return instance

# Productos de guia despacho serializer
class ProductosGuiaDespachoSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProductoDespacho
        fields = ["cantidad", "id_producto"]

# Crear una guia despacho serializer
class CrearGuiaDespachoSerializer(serializers.ModelSerializer):

    productos = ProductosGuiaDespachoSerializer(many=True)

    class Meta:

        model = GuiaDespacho
        fields = ["destino", "id_sucursal", "id_bodeguero", "productos"]

    def create(self, validated_data):

        # Se obtiene los productos enviados
        productos_despacho = validated_data.pop("productos")

        guia_despacho = GuiaDespacho.objects.create(**validated_data) # Se crea una guia despacho

        # Se itera la lista con objetos
        for diccionario in productos_despacho:

            # Se crea un producto despacho por cada objeto que itere
            ProductoDespacho.objects.create(
                cantidad = diccionario["cantidad"],
                id_producto = diccionario["id_producto"],
                id_guia_despacho = guia_despacho
            )

        return guia_despacho

# Actuallizar estado de la guia despacho serializer
class ActualizarEstadoGuiaDespachoSerializer(serializers.ModelSerializer):

    class Meta:

        model = GuiaDespacho
        fields = ["estado"]

    # Metodo de actualizar campos de un modelo Guia Despacho
    def update(self, instance, validated_data):

        instance.estado = validated_data.get("estado", instance.estado)

        instance.save()

        return instance

# Guia Despacho Serializer
class GuiaDespachoSerializer(serializers.ModelSerializer):

    productos = ProductosGuiaDespachoSerializer(many=True)
    id_sucursal = serializers.StringRelatedField()
    id_bodeguero = serializers.StringRelatedField()

    class Meta:

        model = GuiaDespacho
        fields = ["fecha_emicion", "estado", "destino", "productos", "id_sucursal", "id_bodeguero"]

# Factura Serializer
class FacturaSerializer(serializers.ModelSerializer):

    id_proveedor = serializers.StringRelatedField()
    id_bodeguero = serializers.StringRelatedField()

    class Meta:

        model = Factura
        fields = ["code", "fecha_emicion", "productos", "precio_total", "id_proveedor", "id_bodeguero"]

# Crear una factura serializer
class CrearFacturaSerializer(serializers.ModelSerializer):

    # Campos iterables
    pedido = CrearPedidoSerializer(many=False)

    class Meta:

        model = Factura
        fields = ["productos", "id_bodeguero", "id_proveedor", "pedido"]

    # Funcion de realizar validaciones de los json que llegan desde el cliente
    def validate(self, attrs):

        productos = attrs.get("productos")

        # Se valida que el json no puede quedar vacio
        if attrs.get("productos") == {}:
            raise serializers.ValidationError("El json no puede quedar vacio")
        
        # Se hace un control de errores de si el json tiene le parametro "productos"
        try:
            productos_objetos = productos["productos"]
        except KeyError:
            raise serializers.ValidationError("El formato del json no es el correcto")
        
        # Si la lista esta vasia retorna un error
        if productos_objetos == []:
            raise serializers.ValidationError("La lista de los productos no puede estar vacia")

        for producto in productos_objetos:

            if producto.get("nombre") is None:
                raise serializers.ValidationError("Debe requerir un nombre el producto")
            
            if producto.get("cantidad") is None:
                raise serializers.ValidationError("Debe requerir una cantidad el producto")
            
            try:
                int(producto.get("cantidad"))
            except ValueError:
                raise serializers.ValidationError("La cantidad tiene que ser de tipo de dato entero")
            
            if producto.get("cantidad") == 0:
                raise serializers.ValidationError("La cantidad tiene que ser mayor a 0")
            
            if producto.get("precio") is None:
                raise serializers.ValidationError("Debe requerir un precio el producto")
            
            try:
                int(producto.get("precio"))
            except ValueError:
                raise serializers.ValidationError("El precio tiene que ser de tipo de dato entero")
            
            if producto.get("precio") < 1000:
                raise serializers.ValidationError("El precio tiene que ser mayor a 1000 pesos")
            
            break

        return attrs
    
    # Metodo de crear una factura
    def create(self, validated_data):

        # Se obtiene el campo pedido
        destino = validated_data.pop("pedido")

        factura = Factura.objects.create(**validated_data)
        # Se crea un pedido despues de crear una factura
        Pedido.objects.create(
            destino = destino.get("destino"),
            id_factura = factura,
            id_bodeguero = validated_data["id_bodeguero"]
        )

        return factura