from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:

        model = Usuario
        fields = (
            "id",
            "nombre",
            "apellido",
            "username",
            "correo",
            "password",
            "is_active",
            "is_staff",
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):

        usuario = Usuario.objects.create_user(**validated_data)
        return usuario