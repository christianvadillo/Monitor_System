from rest_framework import serializers
from sistema_monitoreo_app.models import Medicion, Error, Recomendacion


class RecomendacionSerializer(serializers.ModelSerializer):
    # Serializer that transform django Recomendacion 'descripcion' field  to json data
    # Used to pass the Recomendacion of the error to to MedicionSerializer using ErrorSerializer
    class Meta:
        model = Recomendacion
        fields = ("descripcion",)


class ErrorSerializer(serializers.ModelSerializer):
    # Serializer that transform django Error object to json data
    # Used to pass the Errors data to MedicionSerializer
    tieneRecomendacion = RecomendacionSerializer(many=True) # With this we add the Recomendacion data from RecomendacionSerializer to the final json object

    class Meta:
        model = Error
        fields = ("id", "nombre", "descripcion", "peligro", "tieneRecomendacion", "es_error_de")


class MedicionSerializer(serializers.ModelSerializer):
    # Serializer that transform django Medicion object to json data
    # Used to get the all data in d3.json call
    tieneError = ErrorSerializer(many=True)  # With this we add the Errors data from ErrorSerializer to the final json object
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Medicion
        fields = "__all__"


class MedicionMinMaxDatesSerializer(serializers.Serializer):
    # Serializer that transform django format date to format %Y-%m-%dT%H:%M:%S
    # Used to get the min date and max date for the d3-dash
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")


# class ReglaSerializer(serializers.Serializer):
#     # Used: False
#     nombre = serializers.CharField()
#     proceso = serializers.CharField()
#     comentario = serializers.CharField()
#     regla = serializers.CharField()
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)
#

