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
    
class ListarSucursalesView(generics.ListCreateAPIView):

    serializer_class = SucursalSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Sucursal.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"data": serializer.data, "message": "Se creo la sucursal con exito"}, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class DetalleSucursalView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = SucursalSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            sucursal = Sucursal.objects.get(id_sucursal = id)
        except Sucursal.DoesNotExist:
            raise Http404

        return sucursal
    
    def get(self, request, id:int, format=None):

        sucursal = self.get_object(id)
        serializer = self.get_serializer(sucursal)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id:int, fromat=None):

        sucursal = self.get_object(id)
        serializer = self.get_serializer(sucursal, data=request.data)

        if not serializer.is_valid():

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"data":serializer.data, "message": "La sucursal a sido actualizada con exito"}, status=status.HTTP_200_OK)

    
    def delete(self, request, id:int, format=None):

        sucursal = self.get_object(id)
        sucursal.delete()

        return Response({"message": "La sucursal a sido eliminada con exito"}, status=status.HTTP_204_NO_CONTENT)
    
class ListarEmpleadosView(generics.ListCreateAPIView):

    serializer_class = EmpleadoSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Empleado.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"data": serializer.data, "message": "Se creo el empleado con exito"}, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class DetalleEmpleadoView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = EmpleadoSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            empleado = Empleado.objects.get(id_empleado = id)
        except Empleado.DoesNotExist:
            raise Http404

        return empleado
    
    def get(self, request, id:int, format=None):

        empleado = self.get_object(id)
        serializer = self.get_serializer(empleado)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id:int, fromat=None):

        empleado = self.get_object(id)
        serializer = self.get_serializer(empleado, data=request.data)

        if not serializer.is_valid():

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"data":serializer.data, "message": "El empleado a sido actualizado con exito"}, status=status.HTTP_200_OK)

    
    def delete(self, request, id:int, format=None):

        empleado = self.get_object(id)
        empleado.delete()

        return Response({"message": "El empleado a sido eliminado con exito"}, status=status.HTTP_204_NO_CONTENT)