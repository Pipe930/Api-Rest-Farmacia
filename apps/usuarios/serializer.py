from rest_framework import serializers
from .models import Usuario, Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = (
            "run",
            "dv",
            "telefono"
        )

class UsuarioSerializer(serializers.ModelSerializer):

    cliente = ClienteSerializer()

    class Meta:

        model = Usuario
        fields = [
            "id",
            "nombre",
            "apellido",
            "username",
            "correo",
            "password",
            "cliente",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):

        cliente_data = validated_data.pop("cliente")
        contrasena = validated_data.pop("password")

        usuario = Usuario.objects.create_user(password=contrasena, **validated_data)
        Cliente.objects.create(
            id_usuario=usuario, 
            correo=usuario.correo, 
            nombre=usuario.nombre, 
            apellido=usuario.apellido, 
            **cliente_data)

        return usuario