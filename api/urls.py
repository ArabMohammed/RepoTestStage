from django.urls import path,include

from . import views
#/api/
urlpatterns=[
    path('',views.load_wilayas_communes),
    path('localisation/',include('api.localisation.urls')),
    path('contacts/',include('api.contacts.urls')),
    path('annonces/',include('api.annonces.urls')),
   path('messages/',include('api.messageoffre.urls')),
]