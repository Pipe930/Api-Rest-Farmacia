from django.views.decorators.csrf import csrf_exempt
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer, String, DateTime, Boolean
from spyne.application import Application
from spyne.decorator import rpc
from spyne.util.django import DjangoComplexModel
from spyne import ComplexModel
from spyne.model.complex import Iterable
from .models import Producto

class ListarProductos(ComplexModel):

    id_producto = Integer
    nombre = String
    precio = Integer
    stock = Integer
    disponible = Boolean
    creado = DateTime
    descripcion = String

    class Attributes(DjangoComplexModel.Attributes):

        django_model = Producto

class ServicioSoapProducto(ServiceBase):

    @rpc(Unicode(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        _returns=Unicode)
    def crear_producto(ctx, nombre, precio, descripcion, id_categoria):

        registro = Producto()

        registro.nombre = nombre
        registro.precio = precio
        registro.descripcion = descripcion
        registro.id_categoria = id_categoria

        registro.save()

        return "Producto Creado: " + nombre
    
    @rpc(Unicode(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        _returns=Unicode)
    def actualizar_producto(ctx, id_producto, nombre, precio, stock, descripcion, id_oferta, id_categoria):

        registro = Producto.objects.get(id_producto=id_producto)

        registro.nombre = nombre
        registro.precio = precio
        registro.stock = stock
        registro.descripcion = descripcion
        registro.id_oferta = id_oferta
        registro.id_categoria = id_categoria

        registro.save()

        return "Producto Creado: " + nombre
    
    @rpc(Unicode(nillable=False), _returns=ListarProductos)
    def obtener_producto(ctx, id_producto):

        producto = Producto.objects.get(id_producto=id_producto)

        return producto
    
    @rpc(_returns=Iterable(ListarProductos))
    def listar_productos(ctx):

        productos = Producto.objects.all()

        return productos
    
    @rpc(Unicode(nillable=False),_returns=Unicode)
    def eliminar_producto(ctx, id_producto):

        producto = Producto.objects.get(id_producto=id_producto)

        producto.delete()

        return "Soap " + id_producto + "eliminado"
    

soap_app_producto = Application(
    [ServicioSoapProducto],
    tns="django.soap.example",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11()
)

django_soap_producto = DjangoApplication(soap_app_producto)
crud_producto = csrf_exempt(django_soap_producto)