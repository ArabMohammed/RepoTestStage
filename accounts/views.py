from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics , mixins ,permissions ,authentication
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserAccount
from .serializers import *
from api.annonces.custom_renderers import PNGRenderer
from api.contacts.models import Contact
from api.localisation.models import Wilaya,Commune

class RegisterView(APIView):
  def post(self, request):
    data = request.data

    serializer = UserCreateSerializer(data=data)

    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.create(serializer.validated_data)
    user = ProfileSerializer(user)
    print("\n")
    print("RegisterView")
    print("\n")
    return Response(user.data, status=status.HTTP_201_CREATED)
##############################################################

class ImageProfileUpdateAPIView(generics.UpdateAPIView):
  serializer_class=UploadProfileImageSerializer
  queryset=UserAccount.objects.all()
  parser_classes = (MultiPartParser, FormParser)
  permission_classes = [permissions.IsAuthenticated]
  def update(self,request,*args,**kwargs):
    print(f'image_url : {request.data.get("image_url")}')
    data_to_change={'profile_image':request.data.get("image_url")}
    serializer=self.serializer_class(request.user,data=data_to_change,partial=True)
    if serializer.is_valid():
      self.perform_update(serializer)
    return Response(serializer.data)

###############################################################
class RetrieveUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]
  def get(self, request):
    print("\n")
    print("RetrieveUserView")
    print("\n")
    user = request.user
    user.is_logged_in=True
    user.save()
    user = ProfileSerializer(user)

    return Response(user.data, status=status.HTTP_200_OK)
###################################
class ProfileUpdateAPIView(generics.UpdateAPIView):
  def update(self,request,*args,**kwargs):
    print("\n")
    print("UpdateUserView")
    print("\n")
    data=request.data
    ###################
    numero_telephone=data.get('numero_telephone')
    date_naissance=data.get('date_naissance')
    nom=data.get("nom")
    prenom=data.get("prenom")
    email=data.get('email')
    #######################################
    modification=0
    user=UserAccount.objects.get(pk=request.user.pk)
    if nom!="":
      if nom!=user.nom :
         #print("modifier nom")
         user.nom=nom
         modification=1

    if prenom!="":
      if prenom!=user.prenom :
         #print("modifier prenom")
         user.prenom=prenom
         modification=1

    if email!="":
      if email!=user.email :
         #print("modifier email")
         user.email=email
         modification=1
    
    if date_naissance!="" :
      print(str(user.date_naissance))
      if str(user.date_naissance)!=date_naissance:
         #print("modifier date naissance")
         user.date_naissance=date_naissance
         modification=1
        
    if numero_telephone!="":
      if user.numero_telephone!=numero_telephone :
         #print("modifier numéro telphone")
         user.numero_telephone=numero_telephone
         modification=1
    wilaya=data.get('wilaya')
    commune=data.get('commune')
    if wilaya != "" and commune !="" :
      if wilaya != user.wilaya.pk or commune != user.commune.pk :
        #print("modifier wilaya and commune")
        user.wilaya=Wilaya.objects.get(pk=wilaya)
        user.commune=Commune.objects.get(pk=commune)
        modification=1
    user.save()##updating user model
    ######################################
    if modification==1 :
       print("\n")
       print("creer nouveau contact")
       print("\n")
       contact=Contact(utilisateur_id=user.pk, email=user.email , nom=user.nom+" "+user.prenom ,
       commune=user.commune,wilaya=user.wilaya,numero_telephone=data.get("numero_telephone"))
       contact.save()
    serializer=ProfileSerializer(request.user)
    print(serializer.data)
    return Response(serializer.data)
###############################################################

class GetImageProfileAPIView(generics.CreateAPIView):
    renderer_classes = [PNGRenderer]    
    def get(self , *args, **kwargs):
        queryset = UserAccount.objects.filter(pk=self.kwargs['id'])[0].profile_image
        data = queryset
        print("image fetched ")
        return Response(data, content_type='image/png')
