from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from api.annonces.models import Annonce
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.localisation.models import *

######################
def load_wilayas_communes(request):
   with open("static/Algerian_WDC.json", "r") as read_file:
      data = json.load(read_file)
      for i in range(0,len(data)):
        wilaya=Wilaya(nom=data[i]["wilaya_name_ascii"],nom_arab=data[i]["wilaya_name_arabe"])
        wilaya.save()
        daira_list=data[i]["Dairas"]
        for j in range(0,len(daira_list)):
            commune_list=daira_list[j]["communes"]
            for k in range(0,len(commune_list)):
                commune=Commune(wilaya_id=i+1,nom=commune_list[k]["commune_name_ascii"],nom_arab=commune_list[k]["commune_name"])
                commune.save()
        nom=data[i]["wilaya_name_ascii"]
        print(f"wilya : {nom} saved")
        print("\n")
   data={"response":"success"}
   return JsonResponse(data)
