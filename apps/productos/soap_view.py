from django.views.decorators.csrf import csrf_exempt
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer, String, DateTime, Boolean
from spyne.application import Application
from spyne.decorator import rpc
from spyne import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.fault import Fault
from .models import Producto

class ListarProductos(ComplexModel):

    id_producto = Integer
    nombre = String
    precio = Integer
    stock = Integer
    disponible = Boolean
    creado = DateTime
    descripcion = String
    id_oferta_id = Integer
    id_categoria_id = Integer

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
        registro.id_categoria_id = id_categoria

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
        
        try:
            registro = Producto.objects.get(id_producto=id_producto)
        except Producto.DoesNotExist as e:
            raise Fault(faultcode=str(e.args[0]), faultstring="Producto no existe")

        registro.nombre = nombre
        registro.precio = precio
        registro.stock = stock
        registro.descripcion = descripcion
        registro.id_oferta_id = id_oferta
        registro.id_categoria_id = id_categoria

        registro.save()

        return "Producto Actualizado: " + nombre
    
    @rpc(Unicode(nillable=False), _returns=ListarProductos)
    def obtener_producto(ctx, id_producto):

        try:
            producto = Producto.objects.get(id_producto=id_producto)
        except Producto.DoesNotExist as e:
            raise Fault(faultcode=str(e.args[0]), faultstring="Producto no existe")

        return producto
    
    @rpc(_returns=Iterable(ListarProductos))
    def listar_productos(ctx):

        productos = Producto.objects.all()

        return productos
    
    @rpc(Unicode(nillable=False),_returns=Unicode)
    def eliminar_producto(ctx, id_producto):
            
        try:
            producto = Producto.objects.get(id_producto=id_producto)
        except Producto.DoesNotExist as e:
            raise Fault(faultcode=str(e.args[0]), faultstring="Producto no existe")

        producto.delete()

        return "Soap " + id_producto + " eliminado"
    

soap_app_producto = Application(
    [ServicioSoapProducto],
    tns="django.soap.example",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11()
)

django_soap_producto = DjangoApplication(soap_app_producto)
crud_producto = csrf_exempt(django_soap_producto)