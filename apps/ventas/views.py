from rest_framework import status, generics
from rest_framework.response import Response
from .models import Carrito, Items, Compra, PedidoCliente
from apps.productos.models import Producto
from django.http import Http404
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
            raise Http404

        return carrito

    def get(self, request, idUser:int, format=None):

        carrito = self.get_object(idUser)

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
            raise Http404

        return product

    def create(self, request):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            data = serializer.data

            producto = self.get_object(data["producto"])

            cantidad = data["cantidad"]

            if producto.stock < cantidad:

                return Response({"message": "La cantidad supera el stock disponible"}, status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({"data": serializer.data, "message": "Agregado al carrito con exito"}, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class RestarCarritoItemView(generics.CreateAPIView):

    serializer_class = RestarCarritoItemSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"message": "Se resto el producto"}, status.HTTP_200_OK)


        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class LimpiarCarritoView(generics.DestroyAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id:int):

        try:
            carrito = Carrito.objects.get(id_carrito=id)
        except Carrito.DoesNotExist:
            raise Http404

        return carrito

    def delete(self, request, id:int, format=None):

        carrito = self.get_object(id)

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

        if serializer.is_valid():

            serializer.save()
            return Response(
                {
                    "data": serializer.data,
                    "message": "Se creo la compra con exito"
                    }, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class CancelarCompraView(generics.UpdateAPIView):

    serializer_class = CancelarCompraSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id:int):

        try:
            compra = Compra.objects.get(id_compra=id)
        except Compra.DoesNotExist:
            raise Http404

        return compra

    def put(self, request, id:int):

        if request.data["estado"]:
            request.data["estado"] = False

        compra = self.get_object(id)
        serializer = CancelarCompraSerializer(compra, data=request.data)

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
            raise Http404

        return compra

    def get(self, request, id:int):

        compra = self.get_object(id)
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

            return Response({"orders": serializer.data}, status.HTTP_200_OK)

        return Response({"message": "No hay pedidos registrados"}, status.HTTP_204_NO_CONTENT)

class DetallePedidoClienteView(generics.RetrieveAPIView):

    serializer_class = PedidoClienteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id:int):

        try:
            pedido_cliente = PedidoCliente.objects.get(id_orden=id)
        except PedidoCliente.DoesNotExist:
            raise Http404

        return pedido_cliente

    def get(self, request, id:int, format=None):

        pedido_cliente = self.get_object(id)
        serializer = self.get_serializer(pedido_cliente)

        return Response(serializer.data, status.HTTP_200_OK)

class CrearPedidoClienteView(generics.CreateAPIView):

    serializer_class = PedidoClienteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    parser_classes = [JSONParser]

    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "data": serializer.data,
                    "message": "pedido creado con exito"
                    }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)