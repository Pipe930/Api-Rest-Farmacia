from rest_framework.response import Response
from rest_framework import generics, status
from .models import Pedido, Proveedor, GuiaDespacho, Bodeguero
from .serializer import PedidoSerializer, BodegueroSerializer, ProveedorSerializer, GuiaDespachoSerializer, CrearPedidoSerializer, ActualizarEstadoPedidoSerializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

class ListarBodeguerosView(generics.ListAPIView):

    serializer_class = BodegueroSerializer
    permission_classes = [AllowAny]
    queryset = Bodeguero.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos bodegueros registrados"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status":"OK","Bodegueros": serializer.data}, status.HTTP_200_OK)
    
class CrearBodegueroView(generics.CreateAPIView):

    serializer_class = BodegueroSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": "Bad Request", 
                    "errors": serializer.errors
                    }, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"data": serializer.data, "status": "Created", "message": "Se creo el bodeguero con exito"}, status.HTTP_201_CREATED)
    
class ListarProveedoresView(generics.ListAPIView):

    serializer_class = ProveedorSerializer
    permission_classes = [AllowAny]
    queryset = Proveedor.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos proveedores registrados"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status":"OK","Proveedores": serializer.data}, status.HTTP_200_OK)
    
class CrearProveedorView(generics.ListAPIView):

    serializer_class = ProveedorSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": "Bad Request", 
                    "errors": serializer.errors
                    }, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"data": serializer.data, "status": "Created", "message": "Se creo el proveedor con exito"}, status.HTTP_201_CREATED)
    
class ListarPedidosView(generics.ListAPIView):

    serializer_class = PedidoSerializer
    permission_classes = [AllowAny]
    queryset = Pedido.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos pedidos registrados"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status":"OK","Bodegueros": serializer.data}, status.HTTP_200_OK)
    
class ListarPedidosView(generics.ListAPIView):

    serializer_class = PedidoSerializer
    permission_classes = [AllowAny]
    queryset = Pedido.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos pedidos registrados"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status":"OK","Bodegueros": serializer.data}, status.HTTP_200_OK)
    
class CrearPedidoView(generics.CreateAPIView):

    serializer_class = CrearPedidoSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                {
                    "status": "Bad Request", 
                    "errors": serializer.errors
                    }, status.HTTP_400_BAD_REQUEST)
        
        productos = request.data["productos"]

        if productos == {}:
            return Response({"message": "El json no puede estar vacio"}, status.HTTP_400_BAD_REQUEST)
        
        try:
            productos["productos"]
        except KeyError:
            return Response({"message": "El json no es valido"}, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {
                "data": serializer.data,
                    "status": "Created", 
                    "message": "El pedido se creo con exito"
                    }, status.HTTP_201_CREATED)
    
class ActualizarEstadoPedidoView(generics.UpdateAPIView):

    serializer_class = ActualizarEstadoPedidoSerializer

    def get_object(self, id:int):

        try:
            pedido = Pedido.objects.get(id_pedido = id)
        except Pedido.DoesNotExist:
            return None

        return pedido

    def put(self, request, id:int, format=None):

        pedido = self.get_object(id)

        if pedido is None:
            return Response(
                {
                    "status": "Not Found", 
                    "message": "Pedido no Encontrado"
                    }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            request.data["estado"]
        except KeyError:
            return Response({"status": "Bad Request","errors": {
                "estado": [
                    "Es te campo es requerido"
                ]
            }}, status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(pedido, data=request.data)

        if not serializer.is_valid():

            return Response(
                {
                    "status": "Bad Request", 
                    "errors": serializer.errors
                    }, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(
            {
                "status": "Update", 
                "message": "El estado del pedido a sido actualizado con exito"
                }, status.HTTP_200_OK)