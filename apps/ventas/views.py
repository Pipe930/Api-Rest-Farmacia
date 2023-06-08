from rest_framework import status, generics
from rest_framework.response import Response
from .models import Carrito, Items, Compra, PedidoCliente
from apps.productos.models import Producto
from .serializer import CarritoSerializer, AgregarCarritoItemSerializer, CancelarCompraSerializer, CompraSerializer, PedidoClienteSerializer, RestarCarritoItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from .total_carrito import calcular_total_cantidad, calcular_total_productos, carrito_total

class CarritoUsuarioView(generics.RetrieveAPIView):

    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, idUser:int):

        try:
            carrito = Carrito.objects.get(id_usuario=idUser)
        except Carrito.DoesNotExist:
            return None

        return carrito

    def get(self, request, idUser:int, format=None):

        carrito = self.get_object(idUser)

        if carrito is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Carrito no Encontrado"
                    }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(carrito)

        return Response(serializer.data, status.HTTP_200_OK)

class AgregarCarritoItemView(generics.CreateAPIView):

    serializer_class = AgregarCarritoItemSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id:int):

        try:
            product = Producto.objects.get(id_producto=id)
        except Producto.DoesNotExist:
            return None

        return product

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        producto = self.get_object(serializer.data["producto"])

        if producto is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Producto no Encontrado"
                    }, status=status.HTTP_404_NOT_FOUND)

        if producto.stock < serializer.data["cantidad"]:

            return Response({"message": "La cantidad supera el stock disponible"}, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"data": serializer.data, "message": "Agregado al carrito con exito"}, status.HTTP_201_CREATED)

class RestarCarritoItemView(generics.CreateAPIView):

    serializer_class = RestarCarritoItemSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"message": "Se resto el producto"}, status.HTTP_200_OK)



class LimpiarCarritoView(generics.DestroyAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id:int):

        try:
            carrito = Carrito.objects.get(id_carrito=id)
        except Carrito.DoesNotExist:
            return None

        return carrito

    def delete(self, request, id:int, format=None):

        carrito = self.get_object(id)

        if carrito is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Carrito no Encontrado"
                    }, status=status.HTTP_404_NOT_FOUND)

        items = Items.objects.filter(id_carrito = carrito.id_carrito)

        if len(items):

            for item in items:
                item.delete()

            carrito_total(carrito)
            calcular_total_cantidad(carrito)
            calcular_total_productos(carrito)

            return Response({"message": "El carrito se a limpiado con exito"}, status.HTTP_204_NO_CONTENT)

        return Response({"message": "Tu carrito esta vacio"}, status.HTTP_204_NO_CONTENT)


class CrearCompraView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    parser_classes = [JSONParser]
    serializer_class = CompraSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(
            {
                "data": serializer.data,
                "message": "Se creo la compra con exito"
                }, status.HTTP_201_CREATED)


class CancelarCompraView(generics.UpdateAPIView):

    serializer_class = CancelarCompraSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id:int):

        try:
            compra = Compra.objects.get(id_compra=id)
        except Compra.DoesNotExist:
            return None

        return compra

    def put(self, request, id:int):

        if request.data["estado"]:
            request.data["estado"] = False

        compra = self.get_object(id)

        if compra is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Compra no Encontrada"
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(compra, data=request.data)

        if serializer.is_valid():

            productos = compra.productos
            items = productos["items"]

            if not compra.estado:
                return Response({"message": "Esta compra esta cancelada"}, status.HTTP_406_NOT_ACCEPTABLE)

            for item in items:

                id = item["id_producto"]
                cantidad = item["cantidad"]
                producto = Producto.objects.get(id_producto=id)

                nuevo_stock = producto.stock + cantidad

                producto.stock = nuevo_stock
                producto.save()

            serializer.save()
            return Response({"message": "Se a cancelado la compra"}, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class ListarComprasView(generics.ListAPIView):

    serializer_class = CompraSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id:int, format=None):

        queryset = Compra.objects.filter(id_usuario=id, estado=True).order_by("creado")
        serializer = self.get_serializer(queryset, many=True)

        if len(serializer.data):

            return Response(serializer.data, status.HTTP_200_OK)

        return Response({"message":"No haz realizado ninguna compra"}, status.HTTP_204_NO_CONTENT)

class DetalleCompraView(generics.RetrieveAPIView):

    serializer_class = CompraSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id:int):

        try:
            compra = Compra.objects.get(id_compra=id)
        except Compra.DoesNotExist:
            return None

        return compra

    def get(self, request, id:int):

        compra = self.get_object(id)

        if compra is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Compra no Encontrada"
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(compra)

        return Response(serializer.data, status.HTTP_200_OK)
    

class ListarPedidosClientesView(generics.ListAPIView):

    queryset = PedidoCliente.objects.all()
    serializer_class = PedidoClienteSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if len(serializer.data):

            return Response({"Ordenes": serializer.data}, status.HTTP_200_OK)

        return Response({"message": "No hay pedidos registrados"}, status.HTTP_204_NO_CONTENT)

class DetallePedidoClienteView(generics.RetrieveAPIView):

    serializer_class = PedidoClienteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id:int):

        try:
            pedido_cliente = PedidoCliente.objects.get(id_pedido=id)
        except PedidoCliente.DoesNotExist:
            return None

        return pedido_cliente

    def get(self, request, id:int, format=None):

        pedido_cliente = self.get_object(id)
        if pedido_cliente is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Compra no Encontrada"
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(pedido_cliente)

        return Response(serializer.data, status.HTTP_200_OK)

class CrearPedidoClienteView(generics.CreateAPIView):

    serializer_class = PedidoClienteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    parser_classes = [JSONParser]

    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {
                "data": serializer.data,
                "message": "Pedido creado con exito"
                }, status=status.HTTP_201_CREATED)