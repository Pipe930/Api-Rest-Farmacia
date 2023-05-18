from rest_framework.response import Response
from rest_framework import generics, status
from django.http import Http404
from .models import Comuna, Provincia, Region, Sucursal, Empleado
from .serializer import ComunaSerializer, ProvinciaSerializer, RegionSerializer, EmpleadoSerializer, SucursalSerializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

class ListarRegionesView(generics.ListCreateAPIView):

    serializer_class = RegionSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Region.objects.all().order_by("nombre")

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"data": serializer.data, "message": "Se creo la region con exito"}, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class ListarProvinciasView(generics.ListCreateAPIView):

    serializer_class = ProvinciaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Provincia.objects.all().order_by("nombre")

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"data": serializer.data, "message": "Se creo la provincia con exito"}, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class ListarComunasView(generics.ListCreateAPIView):

    serializer_class = ComunaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Comuna.objects.all().order_by("nombre")

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"data": serializer.data, "message": "Se creo la comuna con exito"}, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)