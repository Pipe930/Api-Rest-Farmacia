from rest_framework import serializers
from .models import Region, Provincia, Comuna

class RegionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Region
        fields = "__all__"

    def create(self, validated_data):

        region = Region.objects.create(**validated_data)

        return region
    
class ProvinciaSerializer(serializers.ModelSerializer):

    id_region = serializers.StringRelatedField()

    class Meta:

        model = Provincia
        fields = "__all__"
    
class CrearProvinciaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Provincia
        fields = ["nombre", "id_region"]

    def create(self, validated_data):

        provincia = Provincia.objects.create(**validated_data)

        return provincia
    
class ComunaSerializer(serializers.ModelSerializer):

    id_provincia = serializers.StringRelatedField()

    class Meta:

        model = Comuna
        fields = "__all__"
    
class CrearComunaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Comuna
        fields = ["nombre", "id_provincia"]

    def create(self, validated_data):

        comuna = Comuna.objects.create(**validated_data)

        return comuna