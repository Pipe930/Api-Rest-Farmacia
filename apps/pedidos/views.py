from rest_framework.response import Response
from rest_framework import generics, status
from .models import Pedido, Proveedor, GuiaDespacho, Bodeguero, Factura
from .serializer import (
    PedidoSerializer,
    BodegueroSerializer, 
    ProveedorSerializer, 
    GuiaDespachoSerializer, 
    ActualizarEstadoPedidoSerializer, 
    CrearGuiaDespachoSerializer, 
    CrearFacturaSerializer, 
    FacturaSerializer, 
    ActualizarEstadoGuiaDespachoSerializer)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

# --------------------- BODEGUEROS -----------------------------

# Vista para listar todos los bodegueros registrados
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

# Vista para obtener un solo bodeguero
class DetalleBodegueroView(generics.RetrieveAPIView):

    serializer_class = BodegueroSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            bodeguero = Bodeguero.objects.get(id_factura=id)
        except Bodeguero.DoesNotExist:
            return None

        return bodeguero
    
    def get(self, request, id:int, format=None):

        bodeguero = self.get_object(id)

        if bodeguero is None:

            return Response({
                "status": "Not Found",
                "message": "Bodeguero no encontrado"
            }, status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(bodeguero)

        return Response({"status": "OK", "Bodeguero": serializer.data}, status.HTTP_200_OK)

# Vista para crear un bodeguero
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

# --------------------- PROVEEDORES -----------------------------

# Vista para listar todos los proveedores registrados
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
    
class DetalleProveedorView(generics.RetrieveAPIView):

    serializer_class = ProveedorSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            proveedor = Proveedor.objects.get(id_factura=id)
        except Proveedor.DoesNotExist:
            return None

        return proveedor
    
    def get(self, request, id:int, format=None):

        proveedor = self.get_object(id)

        if proveedor is None:

            return Response({
                "status": "Not Found",
                "message": "Proveedor no encontrado"
            }, status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(proveedor)

        return Response({"status": "OK", "Proveedor": serializer.data}, status.HTTP_200_OK)


# Vista para crear un proveedor
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

# --------------------- PEDIDOS -----------------------------

# Vista para listar todos los pedidos
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

        return Response({"status":"OK","Pedidos": serializer.data}, status.HTTP_200_OK)

# Vista para listar los pedidos por factura
class ListarPedidosFacturaView(generics.ListAPIView):

    serializer_class = PedidoSerializer
    permission_classes = [AllowAny]

    def get(self, request, id:int, format=None):

        queryset = Pedido.objects.filter(id_factura=id)
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos pedidos con esa factura"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status":"OK","Pedidos": serializer.data}, status.HTTP_200_OK)

# Vista para obtener un solo pedido
class DetallePedidoView(generics.RetrieveAPIView):

    serializer_class = PedidoSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            pedido = Pedido.objects.get(id_factura=id)
        except Pedido.DoesNotExist:
            return None

        return pedido
    
    def get(self, request, id:int, format=None):

        pedido = self.get_object(id)

        if pedido is None:

            return Response({
                "status": "Not Found",
                "message": "Pedido no encontrado"
            }, status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(pedido)

        return Response({"status": "OK", "Pedido": serializer.data}, status.HTTP_200_OK)

# Vista para actualizar el estado de un pedido
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
        
        # Se hace una pequeña validacion para que el estado sea obligatorio ponerlo
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

# --------------------- FACTURAS -----------------------------

# Vista para listar todas las factura registradas
class ListarFacturasView(generics.ListAPIView):

    serializer_class = FacturaSerializer
    permission_classes = [AllowAny]
    queryset = Factura.objects.all()

    def get(self, request, format=None):

        facturas = self.get_queryset()
        serializer = self.get_serializer(facturas, many=True)

        if not len(serializer.data):

            return Response(
                {
                    "status": "No Content",
                    "message": "No tenemos facturas registradas"
                }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "Facturas": serializer.data}, status.HTTP_200_OK)

# Vista para listar las facturas por proveedor
class FacturasProveedorView(generics.ListAPIView):

    serializer_class = FacturaSerializer
    permission_classes = [AllowAny]

    def get(self, request, id:int, format=None):

        queryset = Factura.objects.filter(id_proveedor=id)
        serializer = self.get_serializer(queryset, many=True)

        if not len(serializer.data):

            return Response(
                {
                    "status": "No Content",
                    "message": "No tenemos facturas con ese proveedor"
                }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "Facturas": serializer.data}, status.HTTP_200_OK)

class DetalleFacturaView(generics.RetrieveAPIView):

    serializer_class = FacturaSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            factura = Factura.objects.get(id_factura=id)
        except Factura.DoesNotExist:
            return None

        return factura
    
    def get(self, request, id:int, format=None):

        factura = self.get_object(id)

        if factura is None:

            return Response({
                "status": "Not Found",
                "message": "Factura no encontrada"
            }, status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(factura)

        return Response({"status": "OK", "Factura": serializer.data}, status.HTTP_200_OK)

# Vista para crear una factura
class CrearFacturaView(generics.CreateAPIView):

    serializer_class = CrearFacturaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            return Response({"status": "Bad Request", "errors" :serializer.errors}, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {
                "data": serializer.data,
                "message": "Se creo la factura con exito",
                "status": "Created"
            }, status.HTTP_201_CREATED)

# --------------------- GUIAS DESPACHO -----------------------------

# Vista para lista todas las guias de despacho registradas
class ListarGuiaDespachoView(generics.ListAPIView):

    serializer_class = GuiaDespachoSerializer
    permission_classes = [AllowAny]
    queryset = GuiaDespacho.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not len(serializer.data):

            return Response(
                {
                    "status": "No Content",
                    "message": "No tenemos guias de despacho registradas"
                }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "Guias Despacho": serializer.data}, status.HTTP_200_OK)

# Vista para listar guias de despacho por sucursal
class ListarGuiaDespachoSucursalView(generics.ListAPIView):

    serializer_class = GuiaDespachoSerializer
    permission_classes = [AllowAny]

    def get(self, request, id:int, format=None):

        queryset = GuiaDespacho.objects.filter(id_sucursal=id)
        serializer = self.get_serializer(queryset, many=True)

        if not len(serializer.data):

            return Response(
                {
                    "status": "No Content",
                    "message": "No tenemos guias de despacho con esa sucursal"
                }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "Guias Despacho": serializer.data}, status.HTTP_200_OK)

# Vista para obtener una sola guia de despacho
class DetalleGuiaDespachoView(generics.RetrieveAPIView):

    serializer_class = GuiaDespachoSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            guia_despacho = GuiaDespacho.objects.get(id_factura=id)
        except GuiaDespacho.DoesNotExist:
            return None

        return guia_despacho
    
    def get(self, request, id:int, format=None):

        guia_despacho = self.get_object(id)

        if guia_despacho is None:

            return Response({
                "status": "Not Found",
                "message": "Guia de Despacho no encontrada"
            }, status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(guia_despacho)

        return Response({"status": "OK", "Guia Despacho": serializer.data}, status.HTTP_200_OK)

# Vista para crear una guia despacho
class CrearGuiaDespachoView(generics.CreateAPIView):

    serializer_class = CrearGuiaDespachoSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                {
                    "status": "Bad Request", 
                    "errors": serializer.errors
                    }, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(
            {
                "status": "Created",
                "data": serializer.data,
                "message": "Se creo la guia de despacho con exito"
                }, status.HTTP_201_CREATED)

# Vista para actualizar el estado de una guia de despacho
class ActualizarEstadoGuiaDespachoView(generics.UpdateAPIView):

    serializer_class = ActualizarEstadoGuiaDespachoSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            guia_despacho = GuiaDespacho.objects.get(id_guia_despacho = id)
        except GuiaDespacho.DoesNotExist:

            return None

        return guia_despacho

    def put(self, request, id:int):

        guia_despacho = self.get_object(id)
        serializer = self.get_serializer(guia_despacho, data=request.data)

        if not serializer.is_valid():
            return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {
                "status": "Update",
                "data": serializer.data,
                "message": "Se actualizo el estado de la guia de despacho con exito"
                }, status.HTTP_200_OK)

