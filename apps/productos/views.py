from rest_framework.response import Response
from rest_framework import generics, status
from django.http import Http404
from .models import Producto, Categoria, Oferta
from .serializer import OfertaSerializer, ProductoSerializer, CategoriaSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

class ListarProductosView(generics.ListCreateAPIView):

    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    pagination_class = LimitOffsetPagination
    queryset = Producto.objects.filter(disponible=True).order_by("nombre")

    def get(self, request, format=None):

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)

        return self.get_paginated_response(serializer.data)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"data": serializer.data, "message": "Se creo el producto con exito"}, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class DetalleProductoView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            producto = Producto.objects.get(id_producto = id)
        except Producto.DoesNotExist:
            raise Http404

        return producto
    
    def get(self, request, id:int, format=None):

        producto = self.get_object(id)
        serializer = self.get_serializer(producto)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id:int, fromat=None):

        producto = self.get_object(id)
        serializer = self.get_serializer(producto, data=request.data)

        if not serializer.is_valid():

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"data":serializer.data, "message": "producto actualizado con exito"}, status=status.HTTP_200_OK)

    
    def delete(self, request, id:int, format=None):

        producto = self.get_object(id)
        producto.delete()

        return Response({"message": "El producto a sido eliminada con exito"}, status=status.HTTP_204_NO_CONTENT)
    
class ListarCategoriasView(generics.ListCreateAPIView):

    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Categoria.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"data": serializer.data, "message": "Se creo la categoria con exito"}, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class DetalleCategoriaView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            categoria = Categoria.objects.get(id_producto = id)
        except Producto.DoesNotExist:
            raise Http404

        return categoria
    
    def get(self, request, id:int, format=None):

        categoria = self.get_object(id)
        serializer = self.get_serializer(categoria)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id:int, fromat=None):

        categoria = self.get_object(id)
        serializer = self.get_serializer(categoria, data=request.data)

        if not serializer.is_valid():

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"data":serializer.data, "message": "categoria actualizado con exito"}, status=status.HTTP_200_OK)

    
    def delete(self, request, id:int, format=None):

        categoria = self.get_object(id)
        categoria.delete()

        return Response({"message": "La categoria a sido eliminada con exito"}, status=status.HTTP_204_NO_CONTENT)
    
class ListarOfertasView(generics.ListCreateAPIView):

    serializer_class = OfertaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Oferta.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"data": serializer.data, "message": "Se creo la oferta con exito"}, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class DetalleOfertaView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = OfertaSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            oferta = Oferta.objects.get(id_producto = id)
        except Producto.DoesNotExist:
            raise Http404

        return oferta
    
    def get(self, request, id:int, format=None):

        oferta = self.get_object(id)
        serializer = self.get_serializer(oferta)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id:int, fromat=None):

        oferta = self.get_object(id)
        serializer = self.get_serializer(oferta, data=request.data)

        if not serializer.is_valid():

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"data":serializer.data, "message": "La oferta se actualizado con exito"}, status=status.HTTP_200_OK)

    
    def delete(self, request, id:int, format=None):

        oferta = self.get_object(id)
        oferta.delete()

        return Response({"message": "La oferta a sido eliminada con exito"}, status=status.HTTP_204_NO_CONTENT)