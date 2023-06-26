from rest_framework.response import Response
from rest_framework import generics, status, filters
from .models import Producto, Categoria, Oferta, Bodega, DetalleBodega
from rest_framework.authentication import TokenAuthentication
from .serializer import ( 
    OfertaSerializer, 
    ProductoSerializer, 
    CategoriaSerializer, 
    BodegaSerialzer, 
    CrearProductoSerializer, 
    ActualizarProductoStockSerializer, 
    StockBodegaSerializer, 
    CrearStockBodegaSerializer, 
    ActualizarOfertaProductoSerializer)
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from farmacia.permission import AdministradorPermission

# --------------------- PRODUCTOS -----------------------------

# Vista para listar todos los productos registrados
class ListarProductosView(generics.ListAPIView):

    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
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

# Vista para listar todos los productos por cierta categoria
class ListarProductoFilterCategoriaView(generics.ListAPIView):

    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
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

# Vista para listar todos los productos por cierta categoria
class ListarProductosOfertaView(generics.ListAPIView):

    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
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

# Vista para buscar productos en base a su nombre
class BuscarProductoView(generics.ListAPIView):

    queryset = Producto.objects.filter(disponible=True).order_by("nombre")
    serializer_class = ProductoSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["nombre"]
    permission_classes = [AllowAny]

# Vista para crear un nuevo producto
class CrearProductoView(generics.CreateAPIView):

    serializer_class = CrearProductoSerializer
    permission_classes = [IsAuthenticated, AdministradorPermission]
    authentication_classes = [TokenAuthentication]
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

# Vista para obtener un solo producto mediante su ID
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

# Vista para actualizar el stock del producto
class ActualizarStockProductoView(generics.UpdateAPIView):

    serializer_class = ActualizarProductoStockSerializer
    permission_classes = [IsAuthenticated, AdministradorPermission]
    authentication_classes = [TokenAuthentication]
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
    
# Vista para actualizar la oferta del producto
class ActualizarOfertaProductoView(generics.UpdateAPIView):

    serializer_class = ActualizarOfertaProductoSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated, AdministradorPermission]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id:int):

        try:
            producto = Producto.objects.get(id_producto = id)
        except Producto.DoesNotExist:
            return None

        return producto

    def put(self, request, id:int, format=None):

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
                "message": "Se actualizo la oferta del producto"
                }, status=status.HTTP_200_OK)

# --------------------- CATEGORIAS -----------------------------

# Vista para listar todas las categorias registradas
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
        
# Vista para obtener una sola categoria
class DetalleCategoriaView(generics.RetrieveAPIView):

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

# --------------------- OFERTAS -----------------------------

# Vista para listar todas las ofertas registradas
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

# Vista para obtener una oferta en base a su ID
class DetalleOfertaView(generics.RetrieveAPIView):

    serializer_class = OfertaSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        try:
            oferta = Oferta.objects.get(id_oferta = id)
        except Oferta.DoesNotExist:
            return None

        return oferta
    
    def get(self, request, id:int, format=None):

        oferta = self.get_object(id)

        if oferta is None:

            return Response(
                {
                    "status": "Not Found", 
                    "message": "Oferta no Encontrada"
                    }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(oferta)

        return Response({"status": "OK", "Oferta":serializer.data}, status=status.HTTP_200_OK)

# --------------------- BODEGAS -----------------------------

# Vista para listar todas las ofertas registradas
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
    

class CrearProductosBodegaView(generics.CreateAPIView):

    serializer_class = CrearStockBodegaSerializer
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

        return Response({"data": serializer.data, "status":"Created","message": "Se creo el detalle bodega con exito"}, status.HTTP_200_OK)


class ListarStockProductosFilterBodegaView(generics.ListAPIView):

    serializer_class = StockBodegaSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):

        bodega = Bodega.objects.get(id_bodega = id)

        return bodega

    def get(self, request, id:int, format=None):

        queryset = DetalleBodega.objects.filter(id_bodega=id)
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos productos con esa bodega"
                    }, status.HTTP_204_NO_CONTENT)
        
        bodega = self.get_object(id)

        return Response(
            {
                "status": "OK", 
                "Bodega": bodega.nombre,
                "Capacidad": bodega.capacidad,
                "Capacidad Ocupada": bodega.capacidad_ocupada,
                "Productos":serializer.data
                }, status=status.HTTP_200_OK)
    
class ListarStockBodegasFilterProductoView(generics.ListAPIView):

    serializer_class = StockBodegaSerializer
    permission_classes = [AllowAny]

    def get(self, request, id:int, format=None):

        queryset = DetalleBodega.objects.filter(id_producto=id)
        serializer = self.serializer_class(queryset, many=True)

        if not len(serializer.data):
            return Response(
                {
                    "status": "No Content", 
                    "message": "No tenemos ese producto en ninguna bodega"
                    }, status.HTTP_204_NO_CONTENT)
        
        stock_total = 0

        for producto in queryset:
            stock_total += producto.stock

        return Response({"status": "OK", "stock_total":stock_total, "Productos":serializer.data}, status=status.HTTP_200_OK)


# def grouper(iterable, n):
#     args = [iter(iterable)] * n
#     return itertools.zip_longest(*args)

# class GeneratePDFView(generics.ListAPIView):
    

#     def get(self, request):
#         # Obtener los datos de la tabla de la base de datos
#         mermas = Merma.objects.all()

#         # Crear un objeto canvas para generar el PDF
#         response = HttpResponse({"message": "PDF generado"}, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="archivo.pdf"'
        
#         p = canvas.Canvas(response)

#         data = [("PRODUCTO", "FECHA EMICION", "CANT. PRODUCTOS", "UBICACION")]

#         p.setFillColorRGB(0.161, 0.255, 0.126)
#         p.drawString(220, 820, "Documento de Merma")
#         # p.rect(50, h - 150, 50, 50, fill=True)

#         for i in mermas:
#             exams = [randint(0, 10) for _ in range(3)]
#             data.append((i.id_producto, i.fecha_emicion, i.cantidad_producto, i.ubicacion))

#         w, h = A4
#         max_rows_per_page = 45
#         # Margin.
#         x_offset = 50
#         y_offset = 50
#         # Space between rows.
#         padding = 15
        
#         xlist = [x + x_offset for x in [0, 80, 180, 300, 400]]
#         ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
        
#         for rows in grouper(data, max_rows_per_page):
#             rows = tuple(filter(bool, rows))
#             p.grid(xlist, ylist[:len(rows) + 1])
#             for y, row in zip(ylist[:-1], rows):
#                 for x, cell in zip(xlist, row):
#                     p.drawString(x + 2, y - padding + 3, str(cell))
#             p.showPage()
        
#         p.save()

#         return response