from django.db import models
from accounts.models import UserAccount
from api.annonces.models import Annonce
from django.utils  import timezone

class Message(models.Model):
    emetteur_id=models.ForeignKey(UserAccount,on_delete=models.PROTECT,related_name='emetteur_messages')
    recepteur_id=models.ForeignKey(UserAccount,on_delete=models.PROTECT,related_name='recepteur_messages')
    annonce_id=models.ForeignKey(Annonce,on_delete=models.CASCADE)
    contenu=models.TextField()
    date_envoi=models.DateField(default=timezone.now,blank=True,null=True)
    #public = models.BooleanField(default=True,blank=True,null=True)
# Create your models here.
