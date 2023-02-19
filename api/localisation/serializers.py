from rest_framework import serializers
from .models import Localisation , Wilaya ,Commune
class LocalisationSerializer(serializers.ModelSerializer):
    class Meta :
        model=Localisation
        fields =[
            'pk',
            'wilaya',
            'commune',
            'adresse_bien_immobilier'
        ]
class WilayaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wilaya
        fields= [
            'pk',
            'nom',
            'nom_arab',
        ]
class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model=Commune
        fields= [
            'pk',
            'wilaya',
            'nom',
            'nom_arab',
        ]