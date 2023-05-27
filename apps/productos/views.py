from rest_framework.response import Response
from rest_framework import generics, status, filters
from .models import Producto, Categoria, Oferta, Bodega, DetalleBodega
from .serializer import OfertaSerializer,ProductoSerializer, CategoriaSerializer, BodegaSerialzer, CrearProductoSerializer, ActualizarProductoStockSerializer, StockBodegaSerializer, CrearStockBodegaSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from datetime import date

class ListarProductosView(generics.ListAPIView):

    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    pagination_class = PageNumberPagination
    queryset = Producto.objects.filter(disponible=True, id_oferta__isnull= True).order_by("nombre")

    def get(self, request, format=None):

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos productos registrados"
                    }, status.HTTP_204_NO_CONTENT)

        return self.get_paginated_response(serializer.data)
    
class ListarProductoFilterCategoriaView(generics.ListAPIView):

    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    pagination_class = PageNumberPagination

    def get(self, request, id:int, format=None):

        queryset = Producto.objects.filter(
            disponible=True, 
            id_oferta__isnull= True, 
            id_categoria=id).order_by("nombre")
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos productos con esa categoria"
                    }, status.HTTP_204_NO_CONTENT)

        return self.get_paginated_response(serializer.data)
    
class ListarProductosOfertaView(generics.ListAPIView):

    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    pagination_class = PageNumberPagination

    def get(self, request, format=None):

        queryset = Producto.objects.filter(
            disponible=True, 
            id_oferta__isnull= False).order_by("nombre")
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos productos en oferta"
                    }, status.HTTP_204_NO_CONTENT)

        return self.get_paginated_response(serializer.data)

class BuscarProductoView(generics.ListAPIView):

    queryset = Producto.objects.filter(disponible=True).order_by("nombre")
    serializer_class = ProductoSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["nombre"]
    permission_classes = [AllowAny]

class CrearProductoView(generics.CreateAPIView):

    serializer_class = CrearProductoSerializer
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

        return Response(
            {
                "data": serializer.data, 
                "status": "Created", 
                "message": "Se creo el producto con exito"
                }, status.HTTP_201_CREATED)

class DetalleProductoView(generics.RetrieveAPIView):

    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            producto = Producto.objects.get(id_producto = id)
        except Producto.DoesNotExist:
            return None

        return producto
    
    def get(self, request, id:int, format=None):

        producto = self.get_object(id)

        if producto is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Producto no Encontrado"
                    }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(producto)

        return Response({"status": "OK", "producto":serializer.data}, status=status.HTTP_200_OK)
    
class ActualizarStockProductoView(generics.UpdateAPIView):

    serializer_class = ActualizarProductoStockSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def get_object(self, id:int):

        try:
            producto = Producto.objects.get(id_producto = id)
        except Producto.DoesNotExist:
            return None

        return producto

    def put(self, request, id:int):

        producto = self.get_object(id)

        if producto is None:
            return Response(
                {
                    "status": "Not Found", 
                    "message": "Producto no Encontrado"
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(producto, data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": "Bad Request", 
                    "errors": serializer.errors
                    }, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(
            {
                "producto":serializer.data, 
                "status": "OK", 
                "message": "Stock del Producto Actualizado"
                }, status=status.HTTP_200_OK)
    
class ListarCategoriasView(generics.ListCreateAPIView):

    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Categoria.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos categorias registradas"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "categorias":serializer.data}, status=status.HTTP_200_OK)
    
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
                "data": serializer.data, 
                "message": "Se creo la categoria con exito",
                "status": "Created"
                }, status.HTTP_201_CREATED)
        

class DetalleCategoriaView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            categoria = Categoria.objects.get(id_categoria = id)
        except Producto.DoesNotExist:
            return None

        return categoria
    
    def get(self, request, id:int, format=None):

        categoria = self.get_object(id)

        if categoria is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Categoria no Encontrada"
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(categoria)

        return Response({"status": "OK", "Categoria":serializer.data}, status=status.HTTP_200_OK)
    
class ListarOfertasView(generics.ListCreateAPIView):

    serializer_class = OfertaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Oferta.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos ofertas registradas"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "Ofertas":serializer.data}, status=status.HTTP_200_OK)
    
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
                "data": serializer.data, 
                "status": "Created", 
                "message": "Se creo la oferta con exito"
                }, status.HTTP_201_CREATED)
    
class DetalleOfertaView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = OfertaSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            oferta = Oferta.objects.get(id_oferta = id)
        except Producto.DoesNotExist:
            return None

        return oferta
    
    def get(self, request, id:int, format=None):

        oferta = self.get_object(id)

        if oferta is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Oferta no Encontrado"
                    }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(oferta)

        return Response({"status": "OK", "Oferta":serializer.data}, status=status.HTTP_200_OK)
    

class ListarBodegasView(generics.ListCreateAPIView):

    serializer_class = BodegaSerialzer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Bodega.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos bodegas registradas"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status":"OK", "Bodegas":serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": "Bad Request", 
                    "errors": serializer.errors
                    }, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"data": serializer.data, "status":"Created","message": "Se creo la bodega con exito"}, status.HTTP_201_CREATED)
    
class DetalleBodegaView(generics.RetrieveAPIView):

    serializer_class = BodegaSerialzer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            bodega = Bodega.objects.get(id_bodega = id)
        except Bodega.DoesNotExist:
            return None

        return bodega
    
    def get(self, request, id:int, format=None):

        bodega = self.get_object(id)

        if bodega is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Bodega no Encontrada"
                    }, status=status.HTTP_404_NOT_FOUND)
    
        serializer = self.get_serializer(bodega)

        return Response({"status": "OK", "Bodega":serializer.data}, status=status.HTTP_200_OK)
    

class CrearProductosBodegaView(generics.ListAPIView):

    serializer_class = CrearStockBodegaSerializer
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

        return Response({"data": serializer.data, "status":"Created","message": "Se creo el detalle bodega con exito"}, status.HTTP_200_OK)


class ListarStockProductosFilterBodegaView(generics.ListAPIView):

    serializer_class = StockBodegaSerializer
    permission_classes = [AllowAny]

    def get(self, request, id:int, format=None):

        queryset = DetalleBodega.objects.filter(id_bodega=id)
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos productos con esa bodega"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "Bodegas":serializer.data}, status=status.HTTP_200_OK)