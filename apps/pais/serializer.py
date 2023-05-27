from rest_framework import serializers
from .models import Region, Provincia, Comuna

# Serializador del Modelo Region
class RegionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Region
        fields = "__all__"

    # Metodo de crear una region
    def create(self, validated_data):

        region = Region.objects.create(**validated_data)

        return region

# Serializador del Modelo Provincia
class ProvinciaSerializer(serializers.ModelSerializer):

    id_region = serializers.StringRelatedField()

    class Meta:

        model = Provincia
        fields = "__all__"

# Serializador de crear un Modelo Provincia
class CrearProvinciaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Provincia
        fields = ["nombre", "id_region"]

    # Metodo crear una provincia
    def create(self, validated_data):

        provincia = Provincia.objects.create(**validated_data)

        return provincia

# Serializador del Modelo Comuna
class ComunaSerializer(serializers.ModelSerializer):

    id_provincia = serializers.StringRelatedField()

    class Meta:

        model = Comuna
        fields = "__all__"

# Serializador de crear un Modelo Comuna
class CrearComunaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Comuna
        fields = ["nombre", "id_provincia"]

    # Metodo crear una comuna
    def create(self, validated_data):

        comuna = Comuna.objects.create(**validated_data)

        return comuna