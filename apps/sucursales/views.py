from rest_framework.response import Response
from rest_framework import generics, status
from .models import Sucursal, Empleado, Cargo
from .serializer import EmpleadoSerializer, SucursalSerializer, CargoSerializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
    
class ListarSucursalesView(generics.ListCreateAPIView):

    serializer_class = SucursalSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Sucursal.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos sucursales registradas"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status":"OK","Sucursales":serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": "Bad Request", 
                    "errors": serializer.errors
                    }, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"data": serializer.data, "status": "Created", "message": "Se creo la sucursal con exito"}, status.HTTP_201_CREATED)
        
    
class DetalleSucursalView(generics.RetrieveAPIView):

    serializer_class = SucursalSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            sucursal = Sucursal.objects.get(id_sucursal = id)
        except Sucursal.DoesNotExist:
            return None

        return sucursal
    
    def get(self, request, id:int, format=None):

        sucursal = self.get_object(id)

        if sucursal is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Sucursal no Encontrada"
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(sucursal)

        return Response({"status":"OK", "Sucursal":serializer.data}, status=status.HTTP_200_OK)
    
class ListarEmpleadosView(generics.ListCreateAPIView):

    serializer_class = EmpleadoSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Empleado.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        
        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos empleados registrados"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status":"OK", "Empleados":serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": "Bad Request", 
                    "errors": serializer.errors
                    }, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"data": serializer.data, "status":"Created", "message": "Se creo el empleado con exito"}, status.HTTP_201_CREATED)
    
class DetalleEmpleadoView(generics.RetrieveAPIView):

    serializer_class = EmpleadoSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            empleado = Empleado.objects.get(id_empleado = id)
        except Empleado.DoesNotExist:
            return None

        return empleado
    
    def get(self, request, id:int, format=None):

        empleado = self.get_object(id)

        if empleado is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Empleado no Encontrado"
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(empleado)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListarCargosView(generics.ListCreateAPIView):

    serializer_class = CargoSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Cargo.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos cargos registrados"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status":"OK","Cargos":serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"data": serializer.data, "message": "Se creo el cargo con exito"}, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class DetalleCargoView(generics.RetrieveUpdateAPIView):

    serializer_class = CargoSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            cargo = Cargo.objects.get(id_cargo = id)
        except Cargo.DoesNotExist:
            return None

        return cargo
    
    def get(self, request, id:int, format=None):

        cargo = self.get_object(id)

        if cargo is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Cargo no Encontrado"
                    }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(cargo)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id:int, fromat=None):

        cargo = self.get_object(id)
        serializer = self.get_serializer(cargo, data=request.data)

        if not serializer.is_valid():

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"data":serializer.data, "message": "El cargo a sido actualizado con exito"}, status=status.HTTP_200_OK)