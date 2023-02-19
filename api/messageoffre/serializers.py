from rest_framework import serializers

from .models import Message
class MessageSerializer(serializers.ModelSerializer):
    class Meta :
        model=Message
        fields =[
           'contenu',
           'annonce_id',
        ]
