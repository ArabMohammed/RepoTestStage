from djoser.serializers import UserCreateSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import models
from .models import UserAccount
from api.localisation.models import Wilaya,Commune
from rest_framework import serializers

User = get_user_model()
###########################

class UserCreateSerializer(UserCreateSerializer):
  class Meta:
    model = User
    fields = ('id','prenom', 'nom', 'email', 'password')

#########################

class UploadProfileImageSerializer(serializers.ModelSerializer):
  class Meta:
    model=UserAccount
    fields=['profile_image']
  def update(self,instance,validated_data):
    instance.profile_image=validated_data.get('profile_image',instance.profile_image)
    instance.save()
    return instance

######################################################"

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model=UserAccount
    fields = ['nom', 'prenom', 'email','date_naissance','wilaya','commune','numero_telephone','pk']

