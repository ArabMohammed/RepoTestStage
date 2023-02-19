from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
#/api/annonces/
urlpatterns =[
    path('loadimage/',views.ImageLoadAPIView.as_view()),
    path('create/',views.AnnonceCreateAPView.as_view()),
    path('list/',views.ImagesListAPView.as_view()),
    path('<id_annonce>/images/<id>',views.ImageAPIView.as_view()),
    #path('<id>/',views.AnnonceDetailAPIView.as_view()),
    path('delete/<id>/',views.AnnonceDeleteAPIView.as_view()),
    path('uploadscrapedannonces/',views.UploadAnnoncesAPIView.as_view()),
    path('research/',views.AnnonceRechercheAPIView.as_view()),

    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)