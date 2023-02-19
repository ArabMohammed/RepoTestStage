from django.shortcuts import render
from django.core.files import File
from rest_framework import generics , mixins ,permissions ,authentication
import json
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ImageAnnonce,Annonce 
from .serializers import  AnnonceCreationSerializer,ImagesSerializer ,ResultatAnnonceSerializer ,DetailAnnonceSerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from .custom_renderers import JPEGRenderer
from accounts.models import UserAccount
from api.contacts.models import Contact
from api.localisation.models import Wilaya ,Commune
from django.db.models import Q
from datetime import date
import requests
from bs4 import BeautifulSoup
from datetime import datetime
###########################################
##########################################
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
          print("success")
class ImageLoadAPIView(generics.CreateAPIView):
    queryset = ImageAnnonce.objects.all()
    serializer_class = ImagesSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        print("perform creation")
        id_annonce=serializer.validated_data.get('id_annonce')
        #print(f'id annonce : {id_annonce}')
        url_image=serializer.validated_data.get('image_url')
        print("creation d'une image")
        #annonce=Annonce.objects.filter(pk=int(id_annonce))
        #print(annonce)
        image=ImageAnnonce(image_url=url_image,id_annonce=id_annonce)
        image.save()


###################################################################
##########To get the number of images of an annonce ##################
################################################################
class ImagesListAPView(generics.ListCreateAPIView):
    def get(self,serializer):
        id_annonce=self.get_queryset()
        queryset = ImageAnnonce.objects.filter(id_annonce__pk=id_annonce)
        data ={"nb_images":len(queryset)}
        return Response(data)
    
    def get_queryset(self):
        annonce_id=self.request.query_params.get('annonce_id')
        return annonce_id
#############################################################

class ImageAPIView(generics.RetrieveAPIView):
    renderer_classes = [JPEGRenderer]
    def get(self, request, *args, **kwargs):
        print("id of image : "+str(self.kwargs['id']))
        print("id of image : "+str(self.kwargs['id_annonce']))
        queryset = ImageAnnonce.objects.filter(id_annonce=int(self.kwargs['id_annonce']))
        print(queryset)
        queryset = ImageAnnonce.objects.filter(id_annonce=int(self.kwargs['id_annonce']))[int(self.kwargs['id'])].image_url
        data = queryset
        print("image fetched ")
        return Response(data, content_type='image/png')

##########################################################

class AnnonceCreateAPView(generics.CreateAPIView):
    queryset=Annonce.objects.all()
    serializer_class=AnnonceCreationSerializer
    def perform_create(self,serializer):
        serializer.save(id_utilisateur=self.request.user)

###########################################################
###########################################################

class AnnonceDeleteAPIView(generics.DestroyAPIView):
    queryset = Annonce.objects.all()
    serializer_class=DetailAnnonceSerializer
    lookup_field='id'

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

############################################################

class AnnonceRechercheAPIView(generics.RetrieveAPIView):
    serializer_class=ResultatAnnonceSerializer     
    def get(self,serializer):
        searchInfo=self.request.query_params
        print(searchInfo)

        ########Recherche selon type ##########
        queryset=Annonce.objects.all()
        first_annonce_date="2018-01-01"
        print(f'first_annonce_date : {first_annonce_date}')
        if searchInfo["search_query"]!="":
           queryset=Annonce.objects.filter(titre__icontains=searchInfo["search_query"].lower())
        if searchInfo["type"]!="":
           queryset=queryset.filter(type_immobilier=searchInfo["type"])
        if searchInfo["categorie"]!="":
           queryset=queryset.filter(categorie_immobilier=searchInfo["categorie"])
        if (searchInfo['wilaya']!=''):
            if(searchInfo["commune"])!='':
               if searchInfo["date_debut"]!='':
                  if searchInfo["date_fin"]!='' :
                    print("\n first \n")
                    queryset=queryset.filter(date_publication__range=(searchInfo['date_debut'],searchInfo['date_fin']))
                    queryset=queryset.filter(wilaya=searchInfo['wilaya'])
                    queryset=queryset.filter(commune=searchInfo['commune'])
                  else :
                    queryset=queryset.filter(date_publication__range=(searchInfo['date_debut'],date.today()))
                    queryset=queryset.filter(wilaya=searchInfo['wilaya'])
                    queryset=queryset.filter(commune=searchInfo['commune'])
                    
               else:
                if searchInfo["date_fin"]!='' :
                    queryset=queryset.filter(date_publication__range=(first_annonce_date,searchInfo['date_fin']))
                    queryset=queryset.filter(wilaya=searchInfo['wilaya'])
                    queryset=queryset.filter(commune=searchInfo['commune'])
                else :
                  queryset=queryset.filter(wilaya=searchInfo['wilaya'])
                  queryset=queryset.filter(commune=searchInfo['commune'])
                   
            else :
                if searchInfo["date_debut"]!='':
                  if searchInfo["date_fin"]!='' :
                    print("second")
                    queryset=queryset.filter(date_publication__range=(searchInfo['date_debut'],searchInfo['date_fin']))
                    queryset=queryset.filter(wilaya=searchInfo['wilaya'])
                  else :
                    queryset=queryset.filter(date_publication__range=(searchInfo['date_debut'],date.today()))
                    queryset=queryset.filter(wilaya=searchInfo['wilaya'])
                 
                else:
                  if searchInfo["date_fin"]!='' :
                    queryset=queryset.filter(date_publication__range=(first_annonce_date,searchInfo['date_fin']))
                    queryset=queryset.filter(wilaya=searchInfo['wilaya'])
                  else :
                    queryset=queryset.filter(wilaya=searchInfo['wilaya'])
        else :
            if searchInfo["date_debut"]!='':
                  if searchInfo["date_fin"]!='' :
                      queryset=queryset.filter(date_publication__range=(searchInfo['date_debut'],searchInfo['date_fin']))
                  else :
                      queryset=queryset.filter(date_publication__range=(searchInfo['date_debut'],date.today())) 
            else:
                if searchInfo["date_fin"]!='' :
                   queryset=queryset.filter(date_publication__range=(first_annonce_date,searchInfo['date_fin'])) 
        final_data=[]
        queryset=queryset.order_by('-date_publication')
        for response in queryset:
            data = ResultatAnnonceSerializer(response).data
            data["nom"]=response.id_utilisateur.nom
            data["prenom"]=response.id_utilisateur.prenom
            final_data.append(data)
        return Response(final_data)
########################################

class AnnonceDetailAPIView(generics.RetrieveAPIView):
    serializer_class=DetailAnnonceSerializer
    def get(self, request, *args, **kwargs):
        queryset = Annonce.objects.get(pk=int(self.kwargs['id']))
        data = DetailAnnonceSerializer(queryset).data
        data['nb_images']=len(ImageAnnonce.objects.filter(id_annonce=self.kwargs['id']))

###################################""

class UploadAnnoncesAPIView(generics.RetrieveAPIView):
    serializer_class=ResultatAnnonceSerializer 
    def get(self,serializer):
        search_info=self.request.query_params
        print(search_info["type"])
        ##############web scraping ###############"
        max_length=7
        list_Annonces=[]
        new_annonce={}
        Site_scraping_url="https://www.annodz.com"
        user_scraper=3
        Site_scraping_url="https://"+search_info["site_annonces"]
        print(f"\n\n\n{Site_scraping_url}")
        for i in range(6,max_length+1): 
           page_url=Site_scraping_url+"/immobilier/"+str(i)
           page=requests.get(page_url)
           soup=BeautifulSoup(page.content,"html.parser")
           results = soup.find_all(class_="cat-ads-wrapper")[0]
           annonces = results.find_all("div",class_="cardbox-show")
           for annonce in annonces :
            titre=annonce.find("h2").text
            description=annonce.find("p").text
            prix=""
            unite_prix=""
            info_prix=annonce.find("div",class_="box-price-show")
            try :
               prix=info_prix.find("span").text
               unite_prix=info_prix.find("span",class_="device").text

               ######################################################

               print("accessing announce page")
               annonce_url=annonce.find("a")["href"]
               announce_page=requests.get(page_url+annonce_url)
               adresse_bien_immobilier=""
               surface=""
               ###############
               soup1=BeautifulSoup(announce_page.content,"html.parser")
               adresse_bien_immobilier= soup1.find("div",class_="sap-i-region").find("span").text
               date_publication= soup1.find("div",class_="sap-i-date").find("span").text
               surface=soup1.find("div",class_="sap-description-critaria").find_all("div",class_="w-50")[1].find("span",class_="ad_info").text
               type_bien=soup1.find("div",class_="sap-description-critaria").find_all("div",class_="w-50")[0].find("span",class_="ad_info").text
               #'''
               #print("welcome1")
               #################
               infos_contact=soup1.find("div",class_="sap-user")
               info1=infos_contact.find("div",class_="sap-profil").find("div",class_="user-profil-infos").find_all("span")
               numero_telephone=infos_contact.find("div",class_="sap-user-action").find("a",class_="phone-link")["href"]
               email=info1[1].text
               nom_prenom=info1[0].find("a").text
               image_link=soup1.find("div",class_="images-fullsize-mobile").find("a")["href"]
               #print("welcome2")
               #######################################
    
               new_annonce={}
               new_annonce["image_link"]=image_link
               new_annonce["unite_prix"]=unite_prix
               new_annonce["prix"]=prix
               new_annonce["type"]=type_bien
               new_annonce["adresse_bien_immobilier"]=adresse_bien_immobilier
               #########"catégorie" à rechercher dans le titre
               new_annonce["titre"]=titre
               new_annonce["description"]=description
               new_annonce["surface"]=surface
               new_annonce["numero_telephone"]=numero_telephone[4:]
               new_annonce["date_publication"]=date_publication[0:10]
               new_annonce["nom"]=nom_prenom
               new_annonce["email"]=email
               #print("welcome3")
               list_Annonces.append(new_annonce)
               #print("welcome4")
            except:
              print("error lors de la recuperaœtion des donnes")
        Nb_annonces_sauvegarde=0
        list_Annonces_scrapes=[]
        for annonce in list_Annonces :
            #########conversion selon le site ###########"
            if annonce["type"].lower()=="studio":
               annonce["type"]="Appartement"
            if annonce["type"].lower()=="Villa":
               annonce["type"]="Maison"
            if annonce["type"].lower()=="local":
               annonce["type"]="Appartement"
            if(annonce["unite_prix"]=="Milliards"):
                annonce["unite_prix"]="Milliard centime"
            if(annonce["unite_prix"]=="Millions"):
                annonce["unite_prix"]="Million centime"
            if(annonce["unite_prix"]=="DA"):
                annonce["unite_prix"]="Da"
            #print(annonce["type"])
            #print(annonce["titre"]) 
            #########################################
            #annonce["type"]==search_info["type"] and
            ################cas 1 categorie != "" et type != ""###################################################""
            if(search_info["categorie"]!="" and search_info["type"]!=""):
                 print("with categorie and type")
                 if annonce["titre"].lower().find(search_info["categorie"].lower())!=-1 and  annonce["type"]==search_info["type"] :
                  id_utilisateur=UserAccount.objects.get(pk=user_scraper)
                  d=str(datetime.strptime(annonce["date_publication"], '%d/%m/%Y'))[0:10]
                  date = str(datetime.strptime(d,'%Y-%m-%d'))[0:10]
                  contact = Contact(utilisateur_id=user_scraper,email=annonce["email"],numero_telephone=annonce["numero_telephone"],nom=annonce["nom"])
                  contact.save()
                  Nb_annonces_sauvegarde=Nb_annonces_sauvegarde+1
                  nouveauAnnonce =Annonce(id_utilisateur=id_utilisateur,titre=annonce["titre"],description=annonce["description"],
                              surface=annonce["surface"],prix=annonce["prix"],date_publication=date,
                              type_immobilier=annonce["type"],categorie_immobilier=search_info["categorie"],
                              unite_prix=annonce["unite_prix"],adresse_bien_immobilier=annonce["adresse_bien_immobilier"],
                              contact=contact,obtenu_webscraping=True)
                  
                  nouveauAnnonce.save()
                  list_Annonces_scrapes.append(nouveauAnnonce)

                  img_url = Site_scraping_url+annonce["image_link"]
                  print(f"ad image :{img_url}")
                  response = requests.get(img_url)
                  if response.status_code==200:
                   print("welcome in saving image")
                   image = response.content
                   with open("image.jpg", "wb") as f:
                     f.write(image)
                   annonce_image=ImageAnnonce(id_annonce=nouveauAnnonce)
                   annonce_image.image_url.save("image.jpg",File(open("image.jpg","rb")))
                   annonce_image.save()
              
            elif search_info["categorie"]!="":
              print("with  categorie")
              if annonce["titre"].lower().find(search_info["categorie"].lower())!=-1 :
                  id_utilisateur=UserAccount.objects.get(pk=user_scraper)
                  d=str(datetime.strptime(annonce["date_publication"], '%d/%m/%Y'))[0:10]
                  date = str(datetime.strptime(d,'%Y-%m-%d'))[0:10]
                  contact = Contact(utilisateur_id=user_scraper,email=annonce["email"],numero_telephone=annonce["numero_telephone"],nom=annonce["nom"])
                  contact.save()
                  Nb_annonces_sauvegarde=Nb_annonces_sauvegarde+1
                  nouveauAnnonce =Annonce(id_utilisateur=id_utilisateur,titre=annonce["titre"],description=annonce["description"],
                              surface=annonce["surface"],prix=annonce["prix"],date_publication=date,
                              type_immobilier=annonce["type"],categorie_immobilier=search_info["categorie"],
                              unite_prix=annonce["unite_prix"],adresse_bien_immobilier=annonce["adresse_bien_immobilier"],
                              contact=contact,obtenu_webscraping=True)
                  
                  nouveauAnnonce.save()
                  list_Annonces_scrapes.append(nouveauAnnonce)
                  
                  img_url = Site_scraping_url+annonce["image_link"]
                  print(f"ad image :{img_url}")
                  response = requests.get(img_url)
                  if response.status_code==200:
                   print("welcome in saving image")
                   image = response.content
                   with open("image.jpg", "wb") as f:
                     f.write(image)
                   annonce_image=ImageAnnonce(id_annonce=nouveauAnnonce)
                   annonce_image.image_url.save("image.jpg",File(open("image.jpg","rb")))
                   annonce_image.save()
              

            elif search_info["type"]!="":
              print("with type")
              if annonce["type"]==search_info["type"] :
                  id_utilisateur=UserAccount.objects.get(pk=user_scraper)
                  d=str(datetime.strptime(annonce["date_publication"], '%d/%m/%Y'))[0:10]
                  date = str(datetime.strptime(d,'%Y-%m-%d'))[0:10]
                  contact = Contact(utilisateur_id=user_scraper,email=annonce["email"],numero_telephone=annonce["numero_telephone"],nom=annonce["nom"])
                  
                  contact.save()

                  Nb_annonces_sauvegarde=Nb_annonces_sauvegarde+1
                  nouveauAnnonce =Annonce(id_utilisateur=id_utilisateur,titre=annonce["titre"],description=annonce["description"],
                              surface=annonce["surface"],prix=annonce["prix"],date_publication=date,
                              type_immobilier=annonce["type"],categorie_immobilier=search_info["categorie"],
                              unite_prix=annonce["unite_prix"],adresse_bien_immobilier=annonce["adresse_bien_immobilier"],
                              contact=contact,obtenu_webscraping=True)
                  
                  nouveauAnnonce.save()
                  list_Annonces_scrapes.append(nouveauAnnonce)
                  
                  img_url = Site_scraping_url+annonce["image_link"]
                  print(f"ad image :{img_url}")
                  response = requests.get(img_url)
                  if response.status_code==200:
                   print("welcome in saving image")
                   image = response.content
                   with open("image.jpg", "wb") as f:
                     f.write(image)
                   annonce_image=ImageAnnonce(id_annonce=nouveauAnnonce)
                   annonce_image.image_url.save("image.jpg",File(open("image.jpg","rb")))
                   annonce_image.save()
            else :
                  print("with no type no categorie")
                  id_utilisateur=UserAccount.objects.get(pk=2)
                  d=str(datetime.strptime(annonce["date_publication"], '%d/%m/%Y'))[0:10]
                  date = str(datetime.strptime(d,'%Y-%m-%d'))[0:10]
                  contact = Contact(utilisateur_id=2,email=annonce["email"],numero_telephone=annonce["numero_telephone"],nom=annonce["nom"])
                  contact.save()
                  Nb_annonces_sauvegarde=Nb_annonces_sauvegarde+1
                  nouveauAnnonce =Annonce(id_utilisateur=id_utilisateur,titre=annonce["titre"],description=annonce["description"],
                              surface=annonce["surface"],prix=annonce["prix"],date_publication=date,
                              type_immobilier=annonce["type"],categorie_immobilier=search_info["categorie"],
                              unite_prix=annonce["unite_prix"],adresse_bien_immobilier=annonce["adresse_bien_immobilier"],
                              contact=contact,obtenu_webscraping=True)
                  
                  nouveauAnnonce.save()
                  list_Annonces_scrapes.append(nouveauAnnonce)
                  
                  img_url = Site_scraping_url+annonce["image_link"]
                  print(f"ad image :{img_url}")
                  response = requests.get(img_url)
                  if response.status_code==200:
                   print("welcome in saving image")
                   image = response.content
                   with open("image.jpg", "wb") as f:
                     f.write(image)
                   annonce_image=ImageAnnonce(id_annonce=nouveauAnnonce)
                   annonce_image.image_url.save("image.jpg",File(open("image.jpg","rb")))
                   annonce_image.save()
        data =DetailAnnonceSerializer(list_Annonces_scrapes,many=True).data
        return Response(data)
                  



