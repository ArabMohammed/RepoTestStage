from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics , mixins ,permissions ,authentication
from .serializers import ContactSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Contact

###########################################

class ContactListAPView(generics.ListCreateAPIView):
    def get(self,serializer):
        queryset = Contact.objects.filter(utilisateur_id=self.request.user.id)
        data =ContactSerializer(queryset,many=True).data
        return Response(data)

##########################################""

class ContactCreateAPView(generics.CreateAPIView):
    queryset=Contact.objects.all()
    serializer_class=ContactSerializer

    def perform_create(self,serializer):
        serializer.save(utilisateur_id=self.request.user)
