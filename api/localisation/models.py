from django.db import models


class Wilaya(models.Model):
    nom = models.CharField(max_length=40)
    nom_arab=models.CharField(max_length=40,blank=True)
    def __str__(self):
        return self.nom
class Commune(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    nom = models.CharField(max_length=40)
    nom_arab=models.CharField(max_length=40,blank=True)

    def __str__(self):
        return self.nom

class Localisation(models.Model):
        wilaya = models.ForeignKey(Wilaya,on_delete=models.PROTECT)
        commune = models.ForeignKey(Commune,on_delete=models.PROTECT)
        adresse_bien_immobilier=models.CharField(max_length=200)
# Create your models here.
