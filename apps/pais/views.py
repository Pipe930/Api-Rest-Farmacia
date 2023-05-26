from rest_framework.response import Response
from rest_framework import generics, status
from .models import Region, Provincia, Comuna
from .serializer import RegionSerializer, ProvinciaSerializer, ComunaSerializer, CrearComunaSerializer, CrearProvinciaSerializer
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

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos regiones registradas"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "regiones": serializer.data}, status.HTTP_200_OK)
    
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {
                "data": serializer.data, 
                "status": "Created", 
                "message": "Se creo la region con exito"
                }, status.HTTP_201_CREATED)
    
class ListarProvinciasView(generics.ListAPIView):

    serializer_class = ProvinciaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Provincia.objects.all().order_by("nombre")

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):

            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos Provincias Registradas"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "provincias":serializer.data}, status.HTTP_200_OK)
    
class ListarProvinciasFilterRegionView(generics.ListAPIView):

    serializer_class = ProvinciaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def get(self, request, id:int, format=None):

        queryset = Provincia.objects.filter(id_region=id).order_by("nombre")
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):

            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos provincias en esa region"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "provincias":serializer.data}, status.HTTP_200_OK)
    
class CrearProvinciaView(generics.CreateAPIView):

    serializer_class = CrearProvinciaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(
            {
                "data": serializer.data, 
                "status": "Created", 
                "message": "Se creo la provincia con exito"
                }, status.HTTP_201_CREATED)

class ListarComunasView(generics.ListAPIView):

    serializer_class = ComunaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Comuna.objects.all().order_by("nombre")

    def get(self, request, format=None):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos comunas registradas"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "comunas":serializer.data}, status.HTTP_200_OK)
    
class ListarComunasFilterProvinciasView(generics.ListAPIView):

    serializer_class = ComunaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def get(self, request, id:int, format=None):

        queryset = Comuna.objects.filter(id_provincia=id).order_by("nombre")
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):

            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos comuna en esa provincia"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status": "OK", "comunas":serializer.data}, status.HTTP_200_OK)

class CrearComunaView(generics.CreateAPIView):

    serializer_class = CrearComunaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(
            {
                "data": serializer.data, 
                "status": "Created", 
                "message": "Se creo la comuna con exito"
                }, status.HTTP_201_CREATED)