from rest_framework.response import Response
from rest_framework import generics, status
from .models import Region, Provincia, Comuna
from .serializer import RegionSerializer, ProvinciaSerializer, ComunaSerializer, CrearComunaSerializer, CrearProvinciaSerializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

# Creacion de las Vistas

# Vista listar todas las regiones registradas
class ListarRegionesView(generics.ListCreateAPIView):

    serializer_class = RegionSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Region.objects.all().order_by("nombre")

    # METODO GET
    def get(self, request, format=None):

        queryset = self.get_queryset() # Se obtiene la query
        serializer = self.serializer_class(queryset, many=True) # Se serializa la queryset

        if not len(serializer.data): # ¿Hay contenido?
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos regiones registradas"
                    }, status.HTTP_204_NO_CONTENT)
        
        # Devuelve la informacion en formato json
        return Response({"status": "OK", "regiones": serializer.data}, status.HTTP_200_OK)
    
    # METODO POST
    def post(self, request, format=None):

        # Se serializa la informacion que llega desde el cliente
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(): # ¿Es valida la informacion?

            # Devuelve un mensaje de error
            return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
        # Se guarda la informacion en la base de datos
        serializer.save()

        # Devuelve la informacion en formatio json
        return Response(
            {
                "data": serializer.data, 
                "status": "Created", 
                "message": "Se creo la region con exito"
                }, status.HTTP_201_CREATED)

# Vista de listar todas las provincias registradas
class ListarProvinciasView(generics.ListAPIView):

    serializer_class = ProvinciaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Provincia.objects.all().order_by("nombre")

    # METODO GET
    def get(self, request, format=None):

        queryset = self.get_queryset() # Se obtiene el query
        serializer = self.serializer_class(queryset, many=True) # Se serializa el queryset

        if not len(serializer.data): # ¿Hay contenido?

            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos Provincias Registradas"
                    }, status.HTTP_204_NO_CONTENT)
        
        # Devuelve la informacion en formato json
        return Response({"status": "OK", "provincias":serializer.data}, status.HTTP_200_OK)

#  Vista de lista de las provincias por region
class ListarProvinciasFilterRegionView(generics.ListAPIView):

    serializer_class = ProvinciaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    # METODO GET
    def get(self, request, id:int, format=None):

        # Se realiza una queryset filtrando las provincas por la region
        queryset = Provincia.objects.filter(id_region=id).order_by("nombre")
        serializer = self.serializer_class(queryset, many=True) # Se serializa la queryset

        if not len(serializer.data): # ¿Hay contenido?

            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos provincias en esa region"
                    }, status.HTTP_204_NO_CONTENT)
        
        # Devuelve la informacion en formato json
        return Response({"status": "OK", "provincias":serializer.data}, status.HTTP_200_OK)

# Vista para crear una provincia  
class CrearProvinciaView(generics.CreateAPIView):

    serializer_class = CrearProvinciaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    # METODO POST
    def post(self, request):

        # Se serializa la infromacion que venga del cliente
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(): # ¿Es valida la informacion?

            return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
        serializer.save() # Se guarda la informacion

        # Devuelve la informacion en formato json
        return Response(
            {
                "data": serializer.data, 
                "status": "Created", 
                "message": "Se creo la provincia con exito"
                }, status.HTTP_201_CREATED)

# Vista de listar todas las comunas registradas
class ListarComunasView(generics.ListAPIView):

    serializer_class = ComunaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Comuna.objects.all().order_by("nombre")

    # METODO GET
    def get(self, request, format=None):

        queryset = self.get_queryset() # Se obtiene la queryset
        serializer = self.serializer_class(queryset, many=True) # Se serializa la queryset

        if not len(serializer.data): # ¿Hay contenido?
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos comunas registradas"
                    }, status.HTTP_204_NO_CONTENT)
        
        # Devuelve la informacion en formato json
        return Response({"status": "OK", "comunas":serializer.data}, status.HTTP_200_OK)

# Vista para listar las comunas por provincia
class ListarComunasFilterProvinciasView(generics.ListAPIView):

    serializer_class = ComunaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    # METODO GET
    def get(self, request, id:int, format=None):

        # Se realiza una queryset filtrando las comunas por la provincia 
        queryset = Comuna.objects.filter(id_provincia=id).order_by("nombre")
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data): # ¿Hay contenido?

            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos comuna en esa provincia"
                    }, status.HTTP_204_NO_CONTENT)
        
        # Devuelve la informacion en formato json
        return Response({"status": "OK", "comunas":serializer.data}, status.HTTP_200_OK)

# Vista para crear una comuna
class CrearComunaView(generics.CreateAPIView):

    serializer_class = CrearComunaSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    # MERODO POST
    def post(self, request):

        # Se serializa la infromacion que venga del cliente
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(): # ¿Es valida la informacion?

            return Response({"status": "Bad Request", "errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
        serializer.save() # Se guarda la informacion

        # Devuelve la informacion en formato json
        return Response(
            {
                "data": serializer.data, 
                "status": "Created", 
                "message": "Se creo la comuna con exito"
                }, status.HTTP_201_CREATED)