from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Annonce ,ImageAnnonce
###################################################
class DetailAnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model= Annonce
        fields =[
            
            'pk',
            'titre',
            'description',
            'prix',
            'surface',

            'categorie_immobilier',
            'type_immobilier',
            'unite_prix',

            'contact',
            'date_publication',

            'wilaya',
            'commune',
            'adresse_bien_immobilier',

            'vendu',
            'public',
            'parking',
            'terrasse',
            'garage',
            'meuble',
            'eau',
            'gaz',
            'electricite',
        ]
##################################################
class ResultatAnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields=[
            'pk',
            'titre',
            'wilaya',
            'commune',
            'adresse_bien_immobilier',
            'date_publication',
        ]
##################################################
class AnnonceRechercheSerializer(serializers.ModelSerializer):
    date_debut=serializers.DateTimeField()
    date_fin=serializers.DateTimeField()
    search_query=serializers.CharField(max_length=100)
    class Meta:
        model=Annonce
        fields=[
            'wilaya',
            'commune',
            'categorie_immobilier',
            'type_immobilier',
            'date_debut',
            'date_fin',
            'search_query'
        ]
###########Annonce###############################
class ImagesSerializer(serializers.ModelSerializer):
    #image_url = serializers.ImageField(required=False)
    #id_annonce=serializers.CharField(max_length=40)
    class Meta:
        model=ImageAnnonce
        fields="__all__"
class AnnonceCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Annonce
        fields =[
            'pk',
            'titre',
            'description',
            'prix',
            'surface',

            'categorie_immobilier',
            'type_immobilier',
            'unite_prix',

            'contact',
            #'localisation',
            'wilaya',
            'commune',
            'adresse_bien_immobilier',
            'vendu',
            'public',
            'parking',
            'terrasse',
            'garage',
            'meuble',
            'eau',
            'gaz',
            'electricite',
        ]