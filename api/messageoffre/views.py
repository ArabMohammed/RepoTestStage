from django.shortcuts import render
from django.shortcuts import render
from django.core.files import File
from rest_framework import generics , mixins ,permissions ,authentication

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from accounts.models import UserAccount
from api.contacts.models import Contact
from api.annonces.models import Annonce
from django.db.models import Q
from datetime import date

from .serializers import MessageSerializer
from .models import Message
###########################################
##########################################

class CreateMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        print("perform creation")
        annonce=serializer.validated_data.get('annonce_id')
        contenu=serializer.validated_data.get('contenu')
        print(f'id annonce : {annonce}')
        recepteur_email=annonce.contact.email
        recepteur_id=UserAccount.objects.get(email=recepteur_email)
        message=Message(annonce_id=annonce,emetteur_id=self.request.user,recepteur_id=recepteur_id,contenu=contenu)
        message.save()
class UpdateBoiteMessageAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,serializer):
        messages=Message.objects.filter(recepteur_id=self.request.user).order_by('-date_envoi')
        list_messages=[]
        new_message={}
        for message in messages :
            new_message={}
            new_message["annonce_id"]=message.annonce_id.pk
            new_message["titre_annonce"]=message.annonce_id.titre
            new_message["emetteur_email"]=message.emetteur_id.email
            new_message["nom"]=message.emetteur_id.nom+" "+message.emetteur_id.prenom
            new_message["date_envoi"]=message.date_envoi
            new_message["contenu"]=message.contenu
            list_messages.append(new_message)
        return Response(list_messages)

class AdministratorDataAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,serializer):
        result={}
        result["Nb_utilisateurs"]=len(UserAccount.objects.all())-1
        result["Nb_annonces"]=len(Annonce.objects.all())
        return Response(result)

