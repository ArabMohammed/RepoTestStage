from django.db import models
from api.localisation.models import Wilaya,Commune
class Contact(models.Model):
        utilisateur_id = models.IntegerField(blank=False)
        nom=models.CharField(max_length=40,blank=True,null=True)
        email=models.EmailField(blank=True,null=True)
        adresse=models.CharField(max_length=200,blank=True,null=True)
        wilaya=models.ForeignKey(Wilaya,on_delete=models.PROTECT,blank=True,null=True)
        commune=models.ForeignKey(Commune,on_delete=models.PROTECT,blank=True,null=True)
        numero_telephone=models.CharField(max_length=15, blank=True ,null=True)


