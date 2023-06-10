from rest_framework.permissions import BasePermission
from apps.usuarios.models import Usuario

class BodegueroPermission(BasePermission):
    def has_permission(self, request, view):
        # Verifica si el usuario tiene el rol de "bodeguero"
        return request.user.rol == 'bodeguero'
    
class EmpleadoPermission(BasePermission):
    def has_permission(self, request, view):
        # Verifica si el usuario tiene el rol de "empleado"
        return request.user.rol == 'empleado'
    
class ClientePermission(BasePermission):
    def has_permission(self, request, view):
        # Verifica si el usuario tiene el rol de "cliente"
        return request.user.rol == 'cliente'

class AdministradorPermission(BasePermission):
    def has_permission(self, request, view):
        # Verifica si el usuario tiene el rol de "administrador"
        return request.user.rol == 'cliente'

def generar_username(nombre, apellido):
    base_username = f"{nombre.lower()}.{apellido.lower()}"
    username = base_username
    contador = 1

    while Usuario.objects.filter(username=username).exists():
        username = f"{base_username}{contador}"
        contador += 1

    return username