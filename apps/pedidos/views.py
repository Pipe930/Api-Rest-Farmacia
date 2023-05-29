from rest_framework.response import Response
from rest_framework import generics, status, filters
from .models import Pedido, Proveedor, GuiaDespacho, Bodeguero
from .serializer import PedidoSerializer, BodegueroSerializer, ProveedorSerializer, GuiaDespachoSerializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

class ListarBodeguerosView(generics.ListAPIView):

    serializer_class = BodegueroSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    queryset = Bodeguero.objects.all()

    def get(self, request, format=None):

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos bodegueros registrados"
                    }, status.HTTP_204_NO_CONTENT)

        return Response({"status":"OK","Bodegueros": serializer.data}, status.HTTP_200_OK)